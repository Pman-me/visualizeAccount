from web3 import Web3


def validate_address(AccountAddress):
    if not Web3.is_address(AccountAddress):
        raise ValueError(f"The address {AccountAddress} is not a valid Ethereum address.")
