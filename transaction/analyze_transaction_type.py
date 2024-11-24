from web3 import Web3

from common.consts import transfer_event_sig_hash, deposit_event_sig_hash, zero_address, \
    withdrawal_event_sig_hash, settings, account_address
from rdbms_utils.sesstion import get_db_session
from repository.redis_repo import RedisRepo
from repository.tx_repo import TxRepo
from transaction.process_bridge import process_bridge_tx, check_if_bridge_tx
from transaction.process_swap import process_swap_tx
from transaction.process_transfer import process_transfer_tx, check_if_transfer_tx
from transaction.save_tx import save_tx
from transaction.transform_tx_data import transform_tx_data
from common.tx_enum import TxType


def categorize_transaction(chain_data: [], txs_per_chain: dict):
    for chain_id, txs in txs_per_chain.items():
        chain = next((chain for chain in chain_data if chain['chain_id'] == chain_id), None)

        w3 = Web3(Web3.HTTPProvider(chain['rpc']))
        api_key = chain['api_key']
        api_endpoint = chain['api_endpoint']
        try:
            for tx in txs:
                tx_receipt = w3.eth.get_transaction_receipt(tx['hash'])
                logs = tx_receipt['logs']
                should_save = False
                send = recv = tx_type = ''

                tx_summary = process_token_transfer_logs(w3, logs)

                if check_if_transfer_tx(w3, tx, logs, tx_summary):
                    should_save = True
                    tx_type = TxType.TRANSFER.value
                    send, recv = process_transfer_tx(w3, api_endpoint, api_key, tx, tx_summary)

                if len(tx_summary.values()) >= 2:
                    should_save = True
                    tx_type = TxType.SWAP.value
                    send, recv = process_swap_tx(w3, api_endpoint=api_endpoint, api_key=api_key,
                                                 tx_summary=tx_summary)

                if check_if_bridge_tx(w3, tx, logs, tx_summary):
                    should_save = True
                    tx_type = TxType.BRIDGE.value
                    send, recv = process_bridge_tx(w3, api_endpoint=api_endpoint, api_key=api_key, tx=tx,
                                                   tx_summary=tx_summary)

                if should_save:
                    save_tx(transform_tx_data(w3, api_endpoint, api_key, l1_fee=tx_receipt['l1Fee'], tx=tx,
                                              tx_type=tx_type,
                                              send=send, recv=recv), tx_repo=TxRepo(session=get_db_session()))
        except (Exception, ValueError) as err:
            pass
        finally:
            RedisRepo(settings.REDIS_HOST, settings.REDIS_PORT).set_hash('max_nonce_per_chain',
                                                                         TxRepo(
                                                                             session=get_db_session()).get_max_nonce_per_chain())


def process_token_transfer_logs(w3: Web3, logs) -> dict:
    """
    Processing token transfer logs and map logs details to transferred token address
    """
    src_dst_per_token_contract = {}
    if logs:
        for log in logs:

            amount = int(log['data'].hex(), 16) if log['data'].hex() != '0x' else 0
            event_sig_hash = int(log['topics'][0].hex(), 16)

            if event_sig_hash == transfer_event_sig_hash:

                if w3.to_checksum_address('0x' + log['topics'][1].hex()[-40:]) == w3.to_checksum_address(
                        account_address) and int(log['topics'][2].hex(), 16) != zero_address:
                    src_dst_per_token_contract[log['address']] = {'from': True, 'amount': amount}

                if w3.to_checksum_address('0x' + log['topics'][2].hex()[-40:]) == w3.to_checksum_address(
                        account_address) and int(log['topics'][1].hex(), 16) != zero_address:
                    src_dst_per_token_contract[log['address']] = {'to': True, 'amount': amount}

            if event_sig_hash == deposit_event_sig_hash:
                src_dst_per_token_contract[log['address']] = {'deposit': True, 'amount': amount}
            if event_sig_hash == withdrawal_event_sig_hash:
                src_dst_per_token_contract[log['address']] = {'withdrawal': True, 'amount': amount}
    return src_dst_per_token_contract
