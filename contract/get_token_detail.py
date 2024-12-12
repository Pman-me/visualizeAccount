import logging

from web3.exceptions import ABIFunctionNotFound

from contract.checking_proxy_contract import is_proxy
from contract.get_contract_detail import get_contract_abi


def get_token_details(w3, api_url, api_key, token_contract_address, log_topics, logger):
    if contract_address := is_proxy(w3, token_contract_address):
        impl_contract_address = contract_address
    else:
        impl_contract_address = token_contract_address

    if abi := get_contract_abi(api_key=api_key, api_url=api_url, contract_address=impl_contract_address):
        token_contract = w3.eth.contract(address=w3.to_checksum_address(token_contract_address), abi=abi)
        try:
            amount = float(log_topics['amount']) / 10 ** token_contract.functions.decimals().call()
            currency = token_contract.functions.symbol().call()
            return amount, currency
        except ABIFunctionNotFound as err:
            logger.error("An error occurred: %s", err)
            return None, None
    return None, None
