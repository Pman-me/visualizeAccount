from web3 import Web3

from contract.get_token_detail import get_token_details


def process_swap_tx(w3: Web3, *, api_url, api_key, tx_summary: dict):
    send = recv = ''

    for token_contract_address, value in tx_summary.items():
        amount, currency = get_token_details(w3, api_url, api_key, token_contract_address, value)

        if amount is not None and currency is not None:
            if value.get('from') or value.get('deposit'):
                send += f'{amount} {currency}' if not send else f', {amount} {currency}'
            elif value.get('to') or value.get('withdrawal'):
                recv = f'{amount} {currency}'
    return send, recv
