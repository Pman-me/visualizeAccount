from pprint import pprint

from web3 import Web3

from consts import account_address
from transaction.nft_transfer_txs import get_nft_transfer_txs_by_address
from transaction.normal_txs import get_normal_txs_by_address


def fetch_txs_per_chain(chain_data: dict, settings) -> dict:
    try:
        tx_per_chain = {}
        for chain in chain_data:

            w3 = Web3(Web3.HTTPProvider(chain['rpc']))
            api_key = chain['api_key']
            api_endpoint = chain['api_endpoint']

            txs = get_normal_txs_by_address(account_address=w3.to_checksum_address(account_address),
                                            endpoint=api_endpoint,
                                            api_key=api_key)
            # nft_transfer_txs = get_nft_transfer_txs_by_address(
            #     account_address=w3.to_checksum_address(account_address),
            #     endpoint=api_endpoint,
            #     api_key=api_key)

            # tx_per_chain[w3.eth.chain_id] = [tx for tx, nft_tx in zip(txs, nft_transfer_txs) if tx['hash'] != nft_tx['hash']]
            tx_per_chain[w3.eth.chain_id] = txs
        return tx_per_chain
    except Exception as e:
        pass
