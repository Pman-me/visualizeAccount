import logging

from web3 import Web3
from transaction.normal_txs import get_normal_txs_by_address


def fetch_txs_per_chain(chain_data: dict, account_address, tx_repo, logger) -> dict:
    try:
        txs_per_chain = {}
        for chain in chain_data:

            w3 = Web3(Web3.HTTPProvider(chain['rpc']))
            api_key = chain['api_key']
            api_url = chain['api_url']

            txs = list(filter(lambda tx: tx['isError'] == "0",
                              get_normal_txs_by_address(account_address=w3.to_checksum_address(account_address),
                                                        api_url=api_url,
                                                        api_key=api_key)))
            if (txs := filter_txs_by_max_nonce(w3, txs, chain_data, account_address, tx_repo)) is not None:
                txs_per_chain[w3.eth.chain_id] = txs

        return txs_per_chain
    except Exception as err:
        logger.error("An error occurred: %s", err)


def filter_txs_by_max_nonce(w3, txs, chain_data: dict, account_address, tx_repo):
    if max_nonce_per_chain := tx_repo.get_max_nonce_per_chain():

        txs_max_nonce = max([int(tx['nonce']) for tx in txs if
                             w3.to_checksum_address(tx['from']) == w3.to_checksum_address(account_address)])

        for item in max_nonce_per_chain:
            if item[1]:
                chain = item[0]
                nonce = int(item[1])

                if chain == next((item['chain'] for item in chain_data if item['chain_id'] == w3.eth.chain_id), None):
                    if txs_max_nonce <= nonce:
                        return None
                    else:
                        txs = list(filter(lambda tx: w3.to_checksum_address(tx['from']) == w3.to_checksum_address(
                            account_address) and int(tx['nonce']) > nonce, txs))
    return txs
