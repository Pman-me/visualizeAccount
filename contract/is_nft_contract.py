from web3.exceptions import ABIFunctionNotFound

from common.check_address_type import is_account_address
from contract.get_contract_detail import get_contract_abi
from settings.si import NFT_INTERFACES_ID


def is_nft_contract(*, w3, api_url, api_key, address, logger):
    if not address:
        return False
    if not is_account_address(w3, address):
        try:
            if abi := get_contract_abi(api_url=api_url, api_key=api_key, contract_address=address, logger=logger):
                contract = w3.eth.contract(address=w3.to_checksum_address(address), abi=abi)
                return any(contract.functions.supportsInterface(eip).call() for eip in NFT_INTERFACES_ID)
        except ABIFunctionNotFound as err:
            logger.error("An error occurred: %s", err)
            return False
    return False
