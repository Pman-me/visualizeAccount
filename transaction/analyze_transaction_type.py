from pprint import pprint

from web3 import Web3

from consts import transfer_event_sig_hash, deposit_event_sig_hash, zero_address, \
    withdrawal_event_sig_hash
from db.sesstion import get_db_session
from repository.tx_repo import TxRepo
from transaction.categorize_swap import specify_swap_data


def save_tx(swap_txs: [], tx_repo: TxRepo):
    for tx in swap_txs:
        pprint(tx)
        tx_repo.set(tx, key=None)


def categorize_transaction(chain_data: [], txs_per_chain: dict):
    for chain_id, txs in txs_per_chain.items():

        chain = next((chain for chain in chain_data if chain['chain_id'] == chain_id), None)

        w3 = Web3(Web3.HTTPProvider(chain['rpc']))
        api_key = chain['api_key']
        api_endpoint = chain['api_endpoint']

        for tx in txs:
            tx_receipt = w3.eth.get_transaction_receipt(tx['hash'])
            if logs := tx_receipt['logs']:
                # fetch src & dst per token transfer in transaction
                src_dst_per_token_contract = analyze_logs_per_tx(w3, logs)
                # find swap type
                if src_dst_per_token_contract:
                    swap_txs = specify_swap_data(w3, api_endpoint=api_endpoint, api_key=api_key,
                                                 data=src_dst_per_token_contract,
                                                 tx=tx, l1_fee=tx_receipt['l1Fee'])

                    save_tx(swap_txs, tx_repo=TxRepo(session=get_db_session()))

            else:
                pass


def analyze_logs_per_tx(w3: Web3, logs, account_address) -> dict:
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
