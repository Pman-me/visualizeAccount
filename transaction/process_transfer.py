from common.check_address_type import is_account_address
from contract.get_token_detail import get_token_details
from settings.si import SCALE, MAX_NONCE_PLATFORM_WALLET


def process_transfer_tx(w3, api_url, api_key, tx, tx_summary, account_address):
    send = recv = None
    if not is_account_address(w3, tx['to']):
        for token_contract_address, value in tx_summary.items():

            amount, currency = get_token_details(w3, api_url, api_key, token_contract_address, value)
            if amount is not None and currency is not None:
                if value.get('from'):
                    send = f"{amount} {currency}"
                if value.get('to'):
                    recv = f"{amount} {currency}"

    if is_account_address(w3, tx['to']):
        if w3.to_checksum_address(tx['to']) == w3.to_checksum_address(account_address):
            recv = f"{float(tx['value']) / SCALE} ETH"
        else:
            send = f"{float(tx['value']) / SCALE} ETH"
    return send, recv


def check_if_transfer_tx(w3, tx, logs, src_dst_per_token_contract):
    """
    To check the transfer of native coins
    It checks that the destination exists,
    if not, it means the contract deployment transaction

    It checks if the nonce of the src and dst wallet addresses is less than a certain value,
    and if it is more, it means that the wallet address is related to a platform(bridge, dex, ...)."""
    return ((tx['to'] and is_account_address(w3, tx['from']) and is_account_address(w3, tx[
        'to']) and not logs and w3.eth.get_transaction_count(
        w3.to_checksum_address(tx['from'])) < MAX_NONCE_PLATFORM_WALLET and w3.eth.get_transaction_count(
        w3.to_checksum_address(tx['to'])) < MAX_NONCE_PLATFORM_WALLET) or (src_dst_per_token_contract and (len(logs) == 1)))
