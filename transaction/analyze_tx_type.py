from web3 import Web3

from common.tx_enum import TxType
from repository.tx_repo import TxRepo
from settings.si import TRANSFER_EVENT_SIG_HASH, ZERO_ADDRESS, DEPOSIT_EVENT_SIG_HASH, \
    WITHDRAWAL_EVENT_SIG_HASH
from transaction.process_bridge import process_bridge_tx, check_if_bridge_tx
from transaction.process_swap import process_swap_tx
from transaction.process_transfer import process_transfer_tx, check_if_transfer_tx
from transaction.save_tx import save_tx
from transaction.transform_tx_data import transform_tx_data


def process_tx(chain_data: [], txs_per_chain: dict, account_address: str, tx_repo: TxRepo):
    for chain_id, txs in txs_per_chain.items():
        chain = next((chain for chain in chain_data if chain['chain_id'] == chain_id), None)

        w3 = Web3(Web3.HTTPProvider(chain['rpc']))
        api_key = chain['api_key']
        api_url = chain['api_url']
        categorize_tx(w3, chain_data=chain_data, txs=txs, api_url=api_url, api_key=api_key, tx_repo=tx_repo,
                      account_address=account_address)


def categorize_tx(w3, *, chain_data, txs, api_url, api_key, tx_repo, account_address):
    try:
        for tx in txs:
            tx_receipt = w3.eth.get_transaction_receipt(tx['hash'])
            logs = tx_receipt['logs']
            should_save = False
            send = recv = tx_type = ''

            tx_summary = process_token_transfer_logs(w3, logs, account_address)

            if check_if_transfer_tx(w3, tx, logs, tx_summary):
                should_save = True
                tx_type = TxType.TRANSFER.value
                send, recv = process_transfer_tx(w3, api_url=api_url, api_key=api_key, tx=tx, tx_summary=tx_summary,
                                                 account_address=account_address)

            if len(tx_summary.values()) >= 2:
                should_save = True
                tx_type = TxType.SWAP.value
                send, recv = process_swap_tx(w3, api_url=api_url, api_key=api_key,
                                             tx_summary=tx_summary)

            if check_if_bridge_tx(w3, tx, logs, tx_summary):
                should_save = True
                tx_type = TxType.BRIDGE.value
                send, recv = process_bridge_tx(w3, api_url=api_url, api_key=api_key, tx=tx,
                                               tx_summary=tx_summary, account_address=account_address)

            if should_save:
                save_tx(transform_tx_data(w3, api_url, api_key, l1_fee=tx_receipt['l1Fee'], tx=tx,
                                          tx_type=tx_type, chain_data=chain_data,
                                          send=send, recv=recv), tx_repo=tx_repo)
    except (Exception, ValueError) as err:
        pass


def process_token_transfer_logs(w3: Web3, logs, account_address) -> dict:
    """
    Processing token transfer logs and map logs details to transferred token address
    """
    src_dst_per_token_contract = {}
    if logs:
        for log in logs:

            amount = int(log['data'].hex(), 16) if log['data'].hex() != '0x' else 0
            event_sig_hash = int(log['topics'][0].hex(), 16)

            if event_sig_hash == TRANSFER_EVENT_SIG_HASH:

                if w3.to_checksum_address('0x' + log['topics'][1].hex()[-40:]) == w3.to_checksum_address(
                        account_address) and int(log['topics'][2].hex(), 16) != ZERO_ADDRESS:
                    src_dst_per_token_contract[log['address']] = {'from': True, 'amount': amount}

                if w3.to_checksum_address('0x' + log['topics'][2].hex()[-40:]) == w3.to_checksum_address(
                        account_address) and int(log['topics'][1].hex(), 16) != ZERO_ADDRESS:
                    src_dst_per_token_contract[log['address']] = {'to': True, 'amount': amount}

            if event_sig_hash == DEPOSIT_EVENT_SIG_HASH:
                src_dst_per_token_contract[log['address']] = {'deposit': True, 'amount': amount}
            if event_sig_hash == WITHDRAWAL_EVENT_SIG_HASH:
                src_dst_per_token_contract[log['address']] = {'withdrawal': True, 'amount': amount}
    return src_dst_per_token_contract
