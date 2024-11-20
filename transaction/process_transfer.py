from check_address_type import is_account_address
from consts import account_address
from contract.get_token_detail import get_token_details


def process_transfer_tx(w3, api_endpoint, api_key, tx, tx_summary):
    send = recv = None
    if not is_account_address(w3, tx['to']):
        for token_contract_address, value in tx_summary.items():
            amount, currency = get_token_details(w3, api_endpoint, api_key, token_contract_address, value)
            if value.get('from'):
                send = f"{amount} {currency}"
            if value.get('to'):
                recv = f"{amount} {currency}"
    if is_account_address(w3, tx['to']):
        if w3.to_checksum_address(tx['to']) == w3.to_checksum_address(account_address):
            recv = f"{float(tx['value']) / 10 ** 18} ETH"
        else:
            send = f"{float(tx['value']) / 10 ** 18} ETH"
    return send, recv


def check_if_transfer_tx(w3, tx, logs, src_dst_per_token_contract):
    """
    To check the transfer of native coins
    It checks that the destination exists,
    if not, it means the contract deployment transaction

    It checks if the number of transactions of the src and dst wallet addresses is less than a certain value,
    and if it is more, it means that the wallet address is related to a platform(bridge, dex, ...)."""
    return ((tx['to'] and is_account_address(w3, tx['from']) and is_account_address(w3, tx[
        'to']) and not logs and w3.eth.get_transaction_count(
        w3.to_checksum_address(tx['from'])) < 20000 and w3.eth.get_transaction_count(
        w3.to_checksum_address(tx['to'])) < 20000) or (src_dst_per_token_contract and (len(logs) == 1)))