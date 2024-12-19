from common.check_address_type import is_account_address
from contract.get_token_detail import get_token_details
from settings.si import MAX_NONCE_PLATFORM_WALLET

from utils.format_token_amount import format_token_amount, get_eth_scaled_value


def process_transfer_tx(*, w3, api_url, api_key, tx, tx_summary, account_address, logger):
    send = recv = ''
    if not is_account_address(w3, tx['to']):
        for token_contract_address, value in tx_summary.items():

            decimals, currency = get_token_details(w3=w3, api_url=api_url, api_key=api_key,
                                                   token_contract_address=token_contract_address,
                                                   logger=logger)
            if decimals is not None and currency is not None:
                if value.get('from'):
                    send = format_token_amount(value['amount'], decimals, currency)
                if value.get('to'):
                    recv = format_token_amount(value['amount'], decimals, currency)

    if is_account_address(w3, tx['to']) and int(tx['value']) > 0:
        if w3.to_checksum_address(tx['to']) == w3.to_checksum_address(account_address):
            recv = get_eth_scaled_value(tx['value'])
        else:
            send = get_eth_scaled_value(tx['value'])
    return send, recv


def check_if_transfer_tx(w3, tx, logs, tx_summary):
    """
    To check the transfer of native coins
    It checks that the destination exists,
    if not, it means the contract deployment transaction

    It checks if the nonce of the src and dst wallet addresses is less than a certain value,
    and if it is more, it means that the wallet address is related to a platform(bridge, dex, ...)."""
    if not tx['to']:
        return False
    return (is_account_address(w3, tx['from'])
            and is_account_address(w3, tx['to'])
            and not logs
            and w3.eth.get_transaction_count(w3.to_checksum_address(tx['from'])) < MAX_NONCE_PLATFORM_WALLET
            and w3.eth.get_transaction_count(w3.to_checksum_address(tx['to'])) < MAX_NONCE_PLATFORM_WALLET
            or (tx_summary and (len(logs) == 1)))
