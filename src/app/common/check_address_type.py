from web3 import Web3


def is_account_address(w3: Web3, address: str):
    if w3.eth.get_code(w3.to_checksum_address(address)) != b'':
        return False
    else:
        return True
