from pprint import pprint

from ethpm.tools.builder import contract_type
from web3 import Web3

from consts import chain_data
from contract.checking_proxy_contract import is_eip1967_proxy, check_unstructured_proxy
from contract.get_contract_detail import get_contract_abi
from save_data import save_tx_data, get_tx_data
from settings import Settings
from transaction.analyze_transaction_type import categorize_transaction
from transaction.txs_data_per_chain import fetch_txs_per_chain


def main():

    # txs = fetch_txs_per_chain(chain_data, settings)
    # save_tx_data(settings, parse_required_tx_data(txs))

    categorize_transaction(chain_data, fetch_txs_per_chain(chain_data, Settings()))

    # w3 = Web3(Web3.HTTPProvider(chain_data[0]['rpc']))
    # api_key = chain_data[0]['api_key']
    # api_endpoint = chain_data[0]['api_endpoint']

    # di = {'0x': {'from': True, 'value': 12},
    #       'sd': {'from': True, 'value': 23},
    #       'ed': {'value': 23},
    #       '03': {'from': True, 'value': 32}}
    # print(categorize_swap(di))


if __name__ == '__main__':
    main()
