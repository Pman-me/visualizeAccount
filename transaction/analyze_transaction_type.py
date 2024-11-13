from web3 import Web3

from consts import transfer_event_sig_hash, deposit_event_sig_hash, zero_address, \
    withdrawal_event_sig_hash, settings, account_address
from db.sesstion import get_db_session
from repository.redis_repo import RedisRepo
from repository.tx_repo import TxRepo
from transaction.process_swap import process_swap_tx
from transaction.process_transfer_tx import process_transfer_tx
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
                processed_txs = []
                tx_receipt = w3.eth.get_transaction_receipt(tx['hash'])

                if logs := tx_receipt['logs']:
                    # fetch src & dst per token transfer in transaction
                    src_dst_per_token_contract = analyze_logs_per_tx(w3, logs)

                    # find swap type
                    if len(src_dst_per_token_contract.values()) >= 2:
                        processed_txs.extend(process_swap_tx(w3, api_endpoint=api_endpoint, api_key=api_key,
                                                             data=src_dst_per_token_contract,
                                                             tx=tx, l1_fee=tx_receipt['l1Fee']))
                    else:
                        send, recv = process_transfer_tx(w3, api_endpoint, api_key, tx, src_dst_per_token_contract,
                                                         len(logs))
                        if send is not None and send is not None:
                            processed_txs.append(
                                transform_tx_data(w3, api_endpoint, api_key, tx_receipt['l1Fee'], tx,
                                                  TxType.TRANSFER.value,
                                                  send, recv))

                    save_tx(processed_txs, tx_repo=TxRepo(session=get_db_session()))
                else:
                    pass
        finally:
            RedisRepo(settings.REDIS_HOST, settings.REDIS_PORT).set_hash('max_nonce_per_chain',
                                                                         TxRepo(
                                                                             session=get_db_session()).get_max_nonce_per_chain())


def analyze_logs_per_tx(w3: Web3, logs) -> dict:
    src_dst_per_token_contract = {}
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
