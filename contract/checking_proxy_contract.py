from web3 import Web3


def check_unstructured_proxy(w3: Web3, address: str):
    impl_slot = '0x'
    impl_address_bytes = w3.eth.get_storage_at(w3.to_checksum_address(address), impl_slot)
    if int.from_bytes(impl_address_bytes, byteorder='big') != 0:
        return w3.to_checksum_address(impl_address_bytes[-20:].hex())
    return None


def is_proxy(w3: Web3, contract_address):

    # 0x360894a13ba1a3210667c828492db98dca3e2076cc3735a920a3ca505d382bbc
    impl_slot = hex(int(w3.keccak(text='eip1967.proxy.implementation').hex(), 16) - 1)
    beacon_slot = hex(int(w3.keccak(text='eip1967.proxy.beacon').hex(), 16) - 1)

    # 0x7050c9e0f4ca769c69bd3a8ef740bc37934f8e2c036e5a723fd8ee048ed3f8c3
    impl_slot_zeppelin = hex(int(w3.keccak(text='org.zeppelinos.proxy.implementation').hex(), 16))
    contract_address = w3.to_checksum_address(contract_address)

    code = w3.eth.get_code(contract_address)
    if len(code) == 0:
        return None

    impl_address_bytes = w3.eth.get_storage_at(contract_address, impl_slot)
    if int(impl_address_bytes.hex(), 16) != 0:
        return w3.to_checksum_address(impl_address_bytes[-20:].hex())

    impl_address_bytes_zeppelin = w3.eth.get_storage_at(contract_address, impl_slot_zeppelin)
    if int(impl_address_bytes_zeppelin.hex(), 16) != 0:
        return w3.to_checksum_address(impl_address_bytes_zeppelin[-20:].hex())

    beacon_address_bytes = w3.eth.get_storage_at(contract_address, beacon_slot)
    if int(beacon_address_bytes.hex(), 16) != 0:
        return w3.to_checksum_address(beacon_address_bytes[-20:].hex())

    return None


