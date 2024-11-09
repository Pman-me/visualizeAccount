from web3 import Web3
from web3.exceptions import ABIFunctionNotFound

from consts import chain_data
from contract.checking_proxy_contract import is_eip1967_proxy
from contract.get_contract_detail import get_contract_abi, get_contract_name
from swap_enum import swap
from transaction.internal_txs import get_internal_txs_by_hash


def specify_swap_data(w3: Web3, *, api_endpoint, api_key, data: dict, tx, l1_fee):
    swap_txs = []
    send = recv = native_currency = native_amount = ""

    for token_contract_address, value in data.items():

        if contract_address := is_eip1967_proxy(w3, token_contract_address):
            impl_contract_address = contract_address
        else:
            impl_contract_address = token_contract_address

        if abi := get_contract_abi(api_key=api_key, api_endpoint=api_endpoint, contract_address=impl_contract_address):

            token_contract = w3.eth.contract(address=w3.to_checksum_address(token_contract_address), abi=abi)
            try:
                amount = float(value['amount']) / 10 ** token_contract.functions.decimals().call()
                currency = token_contract.functions.symbol().call()
            except ABIFunctionNotFound as err:
                print(tx['hash'], data, "ABIFunctionNotFound ***********************")
                continue

            if value.get('from'):
                send += f'{amount} {currency}' if not send else f' {amount} {currency}, '
            elif value.get('to'):
                recv = f'{amount} {currency}'
            elif 'from' not in value and 'to' not in value:
                native_currency = currency
                native_amount = amount

    if native_currency:
        if recv:
            send += f'{native_amount} {native_currency}'
        elif send:

            if internal_txs := get_internal_txs_by_hash(api_endpoint=api_endpoint, api_key=api_key, tx_hash=tx['hash']):

                if filter(lambda _tx: w3.to_checksum_address(_tx['to']) == w3.to_checksum_address(account_address),
                          internal_txs):
                    recv = f'{native_amount} {native_currency}'

    if send and recv:
        swap_txs.append({
            'hash': tx['hash'],
            'from': tx['from'],
            'to_contract_name': get_contract_name(api_key=api_key, api_endpoint=api_endpoint,
                                                  contract_address=tx['to']),
            'input': tx['input'],
            'send': send,
            'recv': recv,
            'nonce': tx['nonce'],
            'timeStamp': tx['timeStamp'],
            'fee': f"{w3.from_wei((int(tx['gasUsed']) * int(tx['gasPrice']) + int(l1_fee, 16)), 'ether'):.10f}",
            'chain': next((item['chain'] for item in chain_data if item['chain_id'] == w3.eth.chain_id), None)
        })
    return swap_txs
