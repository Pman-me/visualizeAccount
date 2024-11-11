import ast

from web3 import Web3

from consts import account_address, settings
from repository.redis_repo import RedisRepo
from transaction.nft_transfer_txs import get_nft_transfer_txs_by_address
from transaction.normal_txs import get_normal_txs_by_address


def fetch_txs_per_chain(chain_data: dict) -> dict:
    try:
        tx_per_chain = {}
        for chain in chain_data:

            w3 = Web3(Web3.HTTPProvider(chain['rpc']))
            api_key = chain['api_key']
            api_endpoint = chain['api_endpoint']

            txs = get_normal_txs_by_address(account_address=w3.to_checksum_address(account_address),
                                            endpoint=api_endpoint,
                                            api_key=api_key)
            if check_max_nonce_exists(w3, txs):
                tx_per_chain[w3.eth.chain_id] = txs
        return tx_per_chain
    except Exception as e:
        pass


def check_max_nonce_exists(w3, txs):
    if (max_nonce_per_chain := RedisRepo(settings.REDIS_HOST, settings.REDIS_PORT).get_list('max_nonce_per_chain')) is not None:
        max_nonce = max([int(tx['nonce']) for tx in txs if
                         w3.to_checksum_address(tx['from']) == w3.to_checksum_address(account_address)])

        for item in max_nonce_per_chain:
            item = ast.literal_eval(item.decode('utf-8'))
            if item[0] == w3.eth.chain_id:
                if max_nonce <= item[1]:
                    return False
                else:
                    for tx in txs:
                        if tx['nonce'] < item[1]:
                            txs.remove(tx)
    return True
