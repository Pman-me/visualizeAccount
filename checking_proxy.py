from web3 import Web3


def check_unstructured_proxy(w3: Web3, address: str):
    impl_slot = '0x0'
    impl_address_bytes = w3.eth.get_storage_at(w3.to_checksum_address(address), impl_slot)
    if int.from_bytes(impl_address_bytes, byteorder='big') != 0:
        return w3.to_checksum_address(impl_address_bytes[-20:].hex())
    return None


def is_eip1967_proxy(w3: Web3, contract_address):
    impl_slot = hex(int(w3.keccak(text='eip1967.proxy.implementation').hex(), 16) - 1)
    beacon_slot = hex(int(w3.keccak(text='eip1967.proxy.beacon').hex(), 16) - 1)

    code = w3.eth.get_code(w3.to_checksum_address(contract_address))
    if len(code) == 0:
        return False

    implementation = w3.eth.get_storage_at(w3.to_checksum_address(contract_address), impl_slot)
    if int(implementation.hex(), 16) != 0:
        return True

    beacon = w3.eth.get_storage_at(w3.to_checksum_address(contract_address), beacon_slot)
    if int(beacon.hex(), 16) != 0:
        return True

    return False


