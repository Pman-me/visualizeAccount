from common.check_address_type import is_account_address
from contract.get_token_detail import get_token_details
from settings.si import SCALE


def process_bridge_tx(w3, api_url, api_key, tx, tx_summary: dict, account_address):
    send = recv = None
    if tx_summary:
        for token_contract_address, value in tx_summary.items():
            amount, currency = get_token_details(w3, api_url, api_key, token_contract_address, value)
            if amount is not None and currency is not None:
                if value.get('from') or value.get('deposit'):
                    send = f"{amount} {currency}"
                if value.get('to') or value.get('withdrawal'):
                    recv = f"{amount} {currency}"
    else:
        if w3.to_checksum_address(tx['from']) == w3.to_checksum_address(account_address):
            send = f"{float(tx['value']) / SCALE} ETH"
        if w3.to_checksum_address(tx['to']) == w3.to_checksum_address(account_address):
            recv = f"{float(tx['value']) / SCALE} ETH"
    return send, recv


def check_if_bridge_tx(w3, tx, logs, tx_summary: dict):
    return ((not logs and (not is_account_address(w3, tx['from']) or not is_account_address(w3, tx['to']))) or
            len(tx_summary) == 1) and tx['value'] != "0" if bool(tx['to']) else False
