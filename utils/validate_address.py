from web3 import Web3


def validate_address(account_address):
    if not Web3.is_address(account_address):
        raise ValueError(f"The address {account_address} is not a valid Ethereum address.")
