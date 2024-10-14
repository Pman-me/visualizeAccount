import json

import requests
from web3 import Web3

from checking_proxy import check_unstructured_proxy, is_eip1967_proxy


def get_contract_name_abi(w3: Web3, tx, *, api_key: str, api_endpoint: str,):
    if impl_address := is_eip1967_proxy(w3, tx['to']):
        contract_address = impl_address
    elif impl_address := check_unstructured_proxy(w3, tx['to']):
        contract_address = impl_address
    else:
        contract_address = tx['to']

    abi_endpoint = f"{api_endpoint}?module=contract&action=getabi&address={contract_address}&apikey={api_key}"
    source_code_endpoint = f"{api_endpoint}?module=contract&action=getsourcecode&address={contract_address}&apikey={api_key}"

    abi = json.loads(requests.get(abi_endpoint).text)

    if type(json.loads(requests.get(source_code_endpoint).text)['result']) is list:
        contract_name = json.loads(requests.get(source_code_endpoint).text)['result'][0]['ContractName']

    if abi['result'] != '':
        contract = w3.eth.contract(address=w3.to_checksum_address('0x1231DEB6f5749EF6cE6943a275A1D3E7486F4EaE'), abi=abi['result'])

        # Decode transaction input
        func_sig, func_args = contract.decode_function_input(tx['input_data'])

        for arg_name, arg_value in func_args.items():
            if isinstance(arg_value, list):
                hex_args = [arg.hex() for arg in arg_value]
                print(hex_args)
            else:
                print(arg_value)

        for i, data_element in enumerate(func_args['data']):
            # Extract function selector & arguments
            selector = data_element[:4]
            args_data = data_element[4:]

        # Decode function input for this data element
        func_sig, func_args = contract.decode_function_input(selector + args_data)
        print('func sig: ', func_sig)
        print('args: ')
        for arg_name, arg_value in func_args.itme():
            print(f' {arg_name}: {arg_value}')

