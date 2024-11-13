from web3 import Web3

from contract.get_token_detail import get_token_details
from transaction.transform_tx_data import transform_tx_data
from tx_enum import TxType


def process_swap_tx(w3: Web3, *, api_endpoint, api_key, data: dict, tx, l1_fee):
    swap_txs = []
    send = recv = ""

    for token_contract_address, value in data.items():
        amount, currency = get_token_details(w3, api_key, api_endpoint, token_contract_address, value)

        if amount is not None and currency is not None:
            if value.get('from') or value.get('deposit'):
                send += f'{amount} {currency}' if not send else f', {amount} {currency}'
            elif value.get('to') or value.get('withdrawal'):
                recv = f'{amount} {currency}'

    if send and recv:
        swap_txs.append(transform_tx_data(w3, api_endpoint, api_key, l1_fee, tx, TxType.SWAP.value, send, recv))
    return swap_txs
