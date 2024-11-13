from check_address_type import is_account_address
from contract.get_token_detail import get_token_details


def process_transfer_tx(w3, api_endpoint, api_key, tx, src_dst_per_token_contract, log_count):
    send = recv = None
    if not is_account_address(w3, tx['to']) and src_dst_per_token_contract.values and log_count == 1:
        for token_contract_address, value in src_dst_per_token_contract.items():
            amount, currency = get_token_details(w3, api_key, api_endpoint, token_contract_address, value)
            if value.get('from'):
                send = f"{amount} {currency}"
            if value.get('to'):
                recv = f"{amount} {currency}"
    if is_account_address(w3, tx['to']):
        send = f"{tx['value']} ETH"
    return send, recv
