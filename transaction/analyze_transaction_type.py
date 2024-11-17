from web3 import Web3

from check_address_type import is_account_address
from consts import transfer_event_sig_hash, deposit_event_sig_hash, zero_address, \
    withdrawal_event_sig_hash, settings, account_address
from db.sesstion import get_db_session
from repository.redis_repo import RedisRepo
from repository.tx_repo import TxRepo
from transaction.process_swap import process_swap_tx
from transaction.process_transfer import process_transfer_tx
from transaction.save_tx import save_tx
from transaction.transform_tx_data import transform_tx_data
from tx_enum import TxType


def categorize_transaction(chain_data: [], txs_per_chain: dict):
    for chain_id, txs in txs_per_chain.items():
        chain = next((chain for chain in chain_data if chain['chain_id'] == chain_id), None)

        w3 = Web3(Web3.HTTPProvider(chain['rpc']))
        api_key = chain['api_key']
        api_endpoint = chain['api_endpoint']
        try:
            for tx in txs:
                should_save = False
                tx_receipt = w3.eth.get_transaction_receipt(tx['hash'])
                logs = tx_receipt['logs']
                send = recv = tx_type = ''

                # fetch src & dst per token transfer in transaction
                src_dst_per_token_contract = analyze_logs_per_tx(w3, logs)

                if check_if_transfer_tx(w3, tx, logs, src_dst_per_token_contract):
                    send, recv = process_transfer_tx(w3, api_endpoint, api_key, tx, src_dst_per_token_contract)
                    tx_type = TxType.TRANSFER.value
                    should_save = True

                if len(src_dst_per_token_contract.values()) >= 2:
                    tx_type = TxType.SWAP.value
                    send, recv = process_swap_tx(w3, api_endpoint=api_endpoint, api_key=api_key,
                                                 data=src_dst_per_token_contract)
                    should_save = True
                if not logs or len(src_dst_per_token_contract) == 1:
                    # May be bridge
                    pass
                if should_save:
                    save_tx(transform_tx_data(w3, api_endpoint, api_key, l1_fee=tx_receipt['l1Fee'], tx=tx,
                                              tx_type=tx_type,
                                              send=send, recv=recv), tx_repo=TxRepo(session=get_db_session()))
        except (Exception, ValueError) as err:
            print(err, tx)
        finally:
            RedisRepo(settings.REDIS_HOST, settings.REDIS_PORT).set_hash('max_nonce_per_chain',
                                                                         TxRepo(
                                                                             session=get_db_session()).get_max_nonce_per_chain())


def check_if_transfer_tx(w3, tx, logs, src_dst_per_token_contract):
    """To check the transfer of native coins
        It checks that the destination exists,
        if not, it means the contract deployment transaction

        It checks if the number of transactions of the src and dst wallet addresses is less than a certain value,
        and if it is more, it means that the wallet address is related to a platform(bridge, dex, ...)."""
    return ((tx['to'] and is_account_address(w3, tx['from']) and is_account_address(w3, tx[
        'to']) and not logs and w3.eth.get_transaction_count(
        w3.to_checksum_address(tx['from'])) < 20000 and w3.eth.get_transaction_count(
        w3.to_checksum_address(tx['to'])) < 20000) or (src_dst_per_token_contract and (len(logs) == 1)))


def analyze_logs_per_tx(w3: Web3, logs) -> dict:
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
