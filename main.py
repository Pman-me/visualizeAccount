import json

import requests
from ens import ENS
from web3 import Web3

from consts import chain_data
from settings import Settings


def get_normal_txs_by_address(account_address: str, endpoint: str, api_key: str) -> list:
    params = {
        'module': 'account',
        'action': 'txlist',
        'address': account_address,
        'startblock': 0,
        'endblock': 99999999,
        'sort': 'asc',
        'apikey': api_key,
        # 'page': 1,
        # 'offset': 10
    }
    data = requests.get(endpoint, params=params).json()
    if data['status'] == '1':
        return data['result']
    else:
        print(data['message'])


def get_nft_transfer_txs_by_address(account_address: str, endpoint: str, api_key: str):
    action_map = {
        'erc721': 'tokennfttx',
        'erc1155': 'token1155tx'
    }
    for token_type, action in action_map.items():
        params = {
            'module': 'account',
            'action': action,
            'address': account_address,
            'startblock': 0,
            'endblock': 99999999,
            'sort': 'asc',
            'apikey': api_key
        }
        data = requests.get(endpoint, params=params).json()
        if data['status'] == '1':
            return data['result']
        else:
            print(data['message'])


def analyze_transaction_type(w3: Web3, ens: ENS, txs, api_endpoint, api_key):
    for tx in txs:
        print(tx)
        if tx.get('tokenDecimal') == '0':
            if tx['from'] == '0x0000000000000000000000000000000000000000':
                # mint
                pass
            elif tx:
                # transfer
                pass
            else:
                # buy or sell
                pass
        else:
            function_name = tx.get('functionName')
            if 'transfer' in function_name:
                # transfer alt coin
                pass
            if function_name == '' or 'deposit' in function_name:
                if is_account_address(w3, tx['to']):
                    # transfer(send) native token to account address
                    pass
                else:
                    # contract(for swap or bridge(with swap or without swap)
                    pass
                pass
            if 'bridge' in function_name:
                get_contract_name_abi(api_endpoint, api_key, tx)

                # print(func_obj, '\t', func_params,)
            if 'swap' in function_name:
                pass


def get_contract_name_abi(w3: Web3, api_endpoint: str, api_key: str, tx: dict):
    abi_endpoint = f"{api_endpoint}?module=contract&action=getabi&address={tx['to']}&apikey={api_key}"
    source_code_endpoint = f"{api_endpoint}?module=contract&action=getsourcecode&address={tx['to']}&apikey={api_key}"

    abi = json.loads(requests.get(abi_endpoint).text)
    contract_name = json.loads(requests.get(source_code_endpoint).text)['result'][0]['ContractName']
    contract = w3.eth.contract(address=w3.to_checksum_address(tx['to']), abi=abi['result'])
    # func_obj, func_params = contract.decode_function_input(tx['input'])


def is_account_address(w3: Web3, address: str):
    if not w3.is_address(address):
        return 'Invalid ethereum address'

    if w3.eth.get_code(w3.to_checksum_address(address)) != b'':
        return False
    else:
        return True


def main():
    settings = Settings()
    try:
        for chain in chain_data:
            rpc = chain['rpc']
            api_key = chain['api_key']
            api_endpoint = chain['api_endpoint']

            w3 = Web3(Web3.HTTPProvider(rpc))
            txs = get_normal_txs_by_address(account_address=w3.to_checksum_address(settings.ACCOUNT_ADDRESS),
                                            endpoint=api_endpoint,
                                            api_key=api_key)
            txs += get_nft_transfer_txs_by_address(account_address=w3.to_checksum_address(settings.ACCOUNT_ADDRESS),
                                                   endpoint=api_endpoint,
                                                   api_key=api_key)

            # analyze_transaction_type(w3, ns, txs, api_endpoint, api_key)
    except Exception as e:
        pass


if __name__ == '__main__':
    main()
