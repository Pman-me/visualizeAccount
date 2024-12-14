from web3.exceptions import ABIFunctionNotFound

from contract.get_contract_detail import get_contract_abi, resolve_contract_address


def get_token_details(*, w3, api_url, api_key, token_contract_address, log_topics, logger):

    if abi := get_contract_abi(api_key=api_key, api_url=api_url,
                               contract_address=resolve_contract_address(w3, token_contract_address), logger=logger):
        token_contract = w3.eth.contract(address=w3.to_checksum_address(token_contract_address), abi=abi)
        try:
            amount = float(log_topics['amount']) / 10 ** token_contract.functions.decimals().call()
            currency = token_contract.functions.symbol().call()
            return amount, currency
        except ABIFunctionNotFound as err:
            logger.error("An error occurred: %s", err)
            return None, None
    return None, None
