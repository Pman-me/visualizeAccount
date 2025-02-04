import json
from functools import lru_cache

import requests

from src.app.common.check_response_status import check_response_status
from src.app.contract.checking_proxy_contract import is_proxy


@lru_cache(maxsize=None, typed=True)
def get_contract_abi(*, api_url: str, api_key: str, contract_address, logger):
    try:
        res = json.loads(
            requests.get(f"{api_url}&module=contract&action=getabi&address={contract_address}&apikey={api_key}").text)
        if res['status'] == '1':
            return res['result']
        return None
    except requests.exceptions.RequestException as err:
        logger.error("An error occurred: %s", err)


def get_contract_name(*, w3, api_url: str, api_key: str, contract_address, logger):

    try:
        res = json.loads(
            requests.get(f"{api_url}&module=contract&action=getsourcecode&address={resolve_contract_address(w3, contract_address)}&apikey={api_key}")
            .text)
        if check_response_status(res):
            return res['result'][0]['ContractName']
        return None
    except requests.exceptions.RequestException as err:
        logger.error("An error occurred: %s %s", err)


def resolve_contract_address(w3, to_addr):
    if impl_address := is_proxy(w3, to_addr):
        contract_address = impl_address
    else:
        contract_address = to_addr
    return contract_address
