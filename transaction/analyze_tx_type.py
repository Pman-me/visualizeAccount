from collections import defaultdict

from web3 import Web3

from common.tx_enum import TxType
from contract.is_nft_contract import is_nft_contract
from repositories.tx_repo import TxRepo
from settings.si import TRANSFER_EVENT_SIG_HASH, DEPOSIT_EVENT_SIG_HASH, \
    WITHDRAWAL_EVENT_SIG_HASH
from transaction.process_bridge import process_bridge_tx, check_if_bridge_tx
from transaction.process_swap import process_swap_tx
from transaction.process_transfer import process_transfer_tx, check_if_transfer_tx
from transaction.save_tx import save_tx
from transaction.transform_tx_data import transform_tx_data


def process_tx(*, chains: [], txs_per_chain: dict, api_base_url: str, api_key: str,
               account_address: str, tx_repo: TxRepo, logger):
    for chain_id, txs in txs_per_chain.items():
        chain = next((chain for chain in chains if chain['chain_id'] == chain_id), None)

        categorize_tx(w3=Web3(Web3.HTTPProvider(chain['rpc'])),
                      txs=txs,
                      api_url=api_base_url + '?chainid=' + str(chain_id),
                      api_key=api_key,
                      tx_repo=tx_repo,
                      account_address=account_address,
                      logger=logger)


def categorize_tx(*, w3, txs, api_url, api_key, tx_repo, account_address, logger):
    try:
        for tx in txs:
            tx_receipt = w3.eth.get_transaction_receipt(tx['hash'])
            logs = tx_receipt['logs']

            if is_nft_contract(w3=w3, api_url=api_url, api_key=api_key, address=tx['to'], logger=logger):
                continue
            tx_summary = process_token_transfer_logs(w3=w3,
                                                     logs=logs, api_url=api_url, api_key=api_key,
                                                     account_address=account_address, logger=logger)
            tx_type, send, recv = determine_tx_type(w3=w3,
                                                    tx=tx, logs=logs, tx_summary=tx_summary, api_url=api_url,
                                                    api_key=api_key, account_address=account_address, logger=logger)
            print(tx_summary, tx['nonce'], tx['hash'])
            if tx_type:
                save_tx(transform_tx_data(w3,
                                          api_url=api_url, api_key=api_key, l1_fee=tx_receipt['l1Fee'], tx=tx,
                                          tx_type=tx_type, account_address=account_address,logger=logger,
                                          send=send, recv=recv), tx_repo=tx_repo)
    except Exception as err:
        logger.error("An error occurred: %s", err)


def determine_tx_type(*, w3, tx, logs, tx_summary, api_url, api_key, account_address, logger):
    send = recv = ''
    tx_type = ''
    result = is_transfer_tx(w3=w3, tx=tx, logs=logs, tx_summary=tx_summary,
                            api_url=api_url, api_key=api_key, account_address=account_address, logger=logger)
    if result[0]:
        tx_type = TxType.TRANSFER.value
        send, recv = result[1], result[2]
        return tx_type, send, recv

    result = is_swap_tx(w3=w3, tx_summary=tx_summary, api_url=api_url, api_key=api_key, logger=logger)
    if result[0]:
        tx_type = TxType.SWAP.value
        send, recv = result[1], result[2]
        return tx_type, send, recv

    result = is_bridge_tx(w3=w3, tx=tx, logs=logs, tx_summary=tx_summary, api_url=api_url,
                          api_key=api_key, account_address=account_address, logger=logger)
    if result[0]:
        tx_type = TxType.BRIDGE.value
        send, recv = result[1], result[2]
        return tx_type, send, recv

    return tx_type, send, recv


def is_swap_tx(*, w3, tx_summary, api_url, api_key, logger):
    if len(tx_summary.values()) >= 2:
        send, recv = process_swap_tx(w3, api_url=api_url, api_key=api_key,
                                     tx_summary=tx_summary, logger=logger)
        return True, send, recv
    return False, '', ''


def is_transfer_tx(*, w3, tx, logs, tx_summary, api_url, api_key, account_address, logger):
    if check_if_transfer_tx(w3, tx, logs, tx_summary):
        send, recv = process_transfer_tx(w3=w3, api_url=api_url, api_key=api_key, tx=tx, tx_summary=tx_summary,
                                         account_address=account_address, logger=logger)
        return True, send, recv
    return False, '', ''


def is_bridge_tx(*, w3, tx, logs, tx_summary, api_url, api_key, account_address, logger):
    if check_if_bridge_tx(w3, tx, logs, tx_summary, api_url, api_key, account_address):
        send, recv = process_bridge_tx(w3, api_url=api_url, api_key=api_key, tx=tx,
                                       tx_summary=tx_summary, account_address=account_address, logger=logger)
        return True, send, recv
    return False, '', ''


def process_token_transfer_logs(*, w3, logs, api_url, api_key, account_address, logger) -> dict:
    """
    Processing token transfer logs and map logs details to transferred token address
    """
    tx_summary = defaultdict(dict)
    if logs:
        for log in logs:
            contract_address = log['address']
            if is_nft_contract(w3=w3, api_url=api_url, api_key=api_key, address=contract_address, logger=logger):
                return {}
            amount = int(log['data'].hex(), 16) if log['data'].hex() != '0x' else 0
            event_sig_hash = int(log['topics'][0].hex(), 16)

            if event_sig_hash == TRANSFER_EVENT_SIG_HASH:

                if w3.to_checksum_address('0x' + log['topics'][1].hex()[-40:]) == w3.to_checksum_address(
                        account_address):
                    # if int(log['topics'][2].hex(), 16) == ZERO_ADDRESS:
                    #     return {}
                    tx_summary[contract_address].update({'from': True, 'amount': amount})

                if w3.to_checksum_address('0x' + log['topics'][2].hex()[-40:]) == w3.to_checksum_address(
                        account_address):
                    # if int(log['topics'][1].hex(), 16) == ZERO_ADDRESS:
                    #     return {}
                    tx_summary[contract_address].update({'to': True, 'amount': amount})

            if event_sig_hash == DEPOSIT_EVENT_SIG_HASH:
                tx_summary[contract_address].update({'deposit': True, 'amount': amount})
            if event_sig_hash == WITHDRAWAL_EVENT_SIG_HASH:
                tx_summary[contract_address].update({'withdrawal': True, 'amount': amount})
    return tx_summary
