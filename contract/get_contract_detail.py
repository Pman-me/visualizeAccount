import json
from functools import lru_cache

import requests
from web3 import Web3

from common.check_response_status import check_response_status
from contract.checking_proxy_contract import is_eip1967_proxy, check_unstructured_proxy


@lru_cache(maxsize=None, typed=True)
def get_contract_abi(*, api_url: str, api_key: str, contract_address):
    try:
        abi_endpoint = f"{api_url}?module=contract&action=getabi&address={contract_address}&apikey={api_key}"
        res = json.loads(requests.get(abi_endpoint).text)

        if res['status'] == '1':
            return res['result']
        return None
    except requests.exceptions.RequestException as e:
        pass


def get_contract_name(*, api_url: str, api_key: str, contract_address):
    try:
        source_code_endpoint = f"{api_url}?module=contract&action=getsourcecode&address={contract_address}&apikey={api_key}"
        res = json.loads(requests.get(source_code_endpoint).text)
        if check_response_status(res):
            return res['result'][0]['ContractName']
        return None
    except requests.exceptions.RequestException as e:
        pass


def get_token_symbol(w3: Web3, *, api_url: str, api_key: str, contract_address):
    contract = w3.eth.contract(address=w3.to_checksum_address(contract_address),
                               abi=get_contract_abi(api_url=api_url, api_key=api_key,
                                                    contract_address=contract_address))
    return contract.functions.symbol().call()


def get_token_decimal(w3: Web3, *, api_url: str, api_key: str, contract_address):
    contract = w3.eth.contract(address=w3.to_checksum_address(contract_address),
                               abi=get_contract_abi(api_url=api_url, api_key=api_key,
                                                    contract_address=contract_address))
    return contract.functions.decimals().call()


def check_contract_address(to_addr, w3):
    if impl_address := is_eip1967_proxy(w3, to_addr):
        contract_address = impl_address
    elif impl_address := check_unstructured_proxy(w3, to_addr):
        contract_address = impl_address
    else:
        contract_address = to_addr
    return contract_address
