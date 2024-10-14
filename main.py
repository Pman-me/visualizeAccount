from pprint import pprint

from web3 import Web3

from analyze_transaction_type import analyze_transaction_type
from checking_proxy import is_eip1967_proxy
from consts import chain_data
from contract_name_abi import get_contract_name_abi
from save_data import save_tx_data, get_tx_data
from settings import Settings
from txs_data_per_chain import fetch_txs_data_per_chain, parse_required_tx_data


def main():
    settings = Settings()
    # txs = fetch_txs_data_per_chain(chain_data, settings)
    # save_tx_data(settings, parse_required_tx_data(txs))
    #
    # analyze_transaction_type(chain_data, list(get_tx_data(settings).values()))

    # w3 = Web3(Web3.HTTPProvider(chain_data[0]['rpc']))
    # api_key = chain_data[1]['api_key']
    # api_endpoint = chain_data[1]['api_endpoint']
    #
    # is_proxy = is_eip1967_proxy(w3, '0xBa5E6fa2f33f3955f0cef50c63dCC84861eAb663')
    # print(f"Is EIP-1967 proxy: {is_proxy}")


if __name__ == '__main__':
    main()
