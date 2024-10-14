from web3 import Web3

from nft_transfer_txs import get_nft_transfer_txs_by_address
from normal_txs import get_normal_txs_by_address


def fetch_txs_data_per_chain(chain_data: dict, settings) -> dict:
    try:
        tx_per_chain = dict()
        for chain in chain_data:

            w3 = Web3(Web3.HTTPProvider(chain['rpc']))
            api_key = chain['api_key']
            api_endpoint = chain['api_endpoint']

            txs = get_normal_txs_by_address(account_address=w3.to_checksum_address(settings.ACCOUNT_ADDRESS),
                                            endpoint=api_endpoint,
                                            api_key=api_key)
            txs += get_nft_transfer_txs_by_address(
                account_address=w3.to_checksum_address(settings.ACCOUNT_ADDRESS),
                endpoint=api_endpoint,
                api_key=api_key)
            tx_per_chain[w3.eth.chain_id] = txs
        return tx_per_chain
    except Exception as e:
        pass


def parse_required_tx_data(map_chain_txs: dict) -> []:
    all_tx_data = []
    for chain_id, txs in map_chain_txs.items():
        for tx in txs:
            tx_data_per_chain = dict()
            tx_data_per_chain['hash'] = tx['hash']
            tx_data_per_chain['from'] = tx['from']
            tx_data_per_chain['to'] = tx['to']
            tx_data_per_chain['block_number'] = tx['blockNumber']
            tx_data_per_chain['nonce'] = tx['nonce']
            tx_data_per_chain['value'] = tx.get('value')
            tx_data_per_chain['timestamp'] = tx['timeStamp']
            tx_data_per_chain['input_data'] = tx.get('input')
            tx_data_per_chain['tokenDecimal'] = tx.get('tokenDecimal')
            tx_data_per_chain['chain_id'] = chain_id

            all_tx_data.append(tx_data_per_chain)
    return all_tx_data
