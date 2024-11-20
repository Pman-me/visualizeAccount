import ast

from web3 import Web3

from consts import account_address, settings, chain_data
from repository.redis_repo import RedisRepo
from transaction.normal_txs import get_normal_txs_by_address


def fetch_txs_per_chain() -> dict:
    try:
        txs_per_chain = {}
        for chain in chain_data:

            w3 = Web3(Web3.HTTPProvider(chain['rpc']))
            api_key = chain['api_key']
            api_endpoint = chain['api_endpoint']

            txs = list(filter(lambda tx: tx['isError'] == "0",
                              get_normal_txs_by_address(account_address=w3.to_checksum_address(account_address),
                                                        endpoint=api_endpoint,
                                                        api_key=api_key)))
            if (txs := filter_txs_by_max_nonce(w3, txs)) is not None:
                txs_per_chain[w3.eth.chain_id] = txs
        return txs_per_chain
    except Exception as e:
        pass


def filter_txs_by_max_nonce(w3, txs):
    if (max_nonce_per_chain := RedisRepo(settings.REDIS_HOST, settings.REDIS_PORT).get_hash(
            'max_nonce_per_chain')):
        max_nonce = max([int(tx['nonce']) for tx in txs if
                         w3.to_checksum_address(tx['from']) == w3.to_checksum_address(account_address)])

        for key, value in max_nonce_per_chain.items():
            value = ast.literal_eval(value.decode('utf-8'))

            if key.decode('utf-8') == next(
                    (item['chain'] for item in chain_data if item['chain_id'] == w3.eth.chain_id), None):
                if max_nonce <= value:
                    return None
                else:
                    txs = list(filter(lambda tx: w3.to_checksum_address(tx['from']) == w3.to_checksum_address(
                        account_address) and int(tx['nonce']) > value, txs))
    return txs
