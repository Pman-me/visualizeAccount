from common.check_address_type import is_account_address
from contract.get_token_detail import get_token_details
from settings.si import MAX_NONCE_PLATFORM_WALLET
from transaction.internal_txs import get_internal_txs_by_hash
from utils.format_token_amount import get_eth_scaled_value, format_token_amount


def process_bridge_tx(w3, api_url, api_key, tx, tx_summary, account_address, logger):
    send = recv = ''
    if tx_summary:
        for token_contract_address, value in tx_summary.items():
            decimals, currency = get_token_details(w3=w3, api_url=api_url, api_key=api_key,
                                                   token_contract_address=token_contract_address,
                                                   logger=logger)
            if decimals is not None and currency is not None:
                if value.get('from'):
                    send += format_token_amount(value['amount'], decimals,
                                                currency) if not send else ', ' + format_token_amount(value['amount'],
                                                                                                      decimals,
                                                                                                      currency)
                if value.get('to'):
                    recv = format_token_amount(value['amount'], decimals, currency)

    if (not tx_summary or any('deposit' in nested_dict for nested_dict in tx_summary.values()) or
            any('withdrawal' in nested_dict for nested_dict in tx_summary.values())):
        if w3.to_checksum_address(tx['from']) == w3.to_checksum_address(account_address):
            send = get_eth_scaled_value(tx['value']) if not send else ', ' + get_eth_scaled_value(tx['value'])
        if w3.to_checksum_address(tx['to']) == w3.to_checksum_address(account_address):
            recv = get_eth_scaled_value(tx['value'])
    return send, recv


def check_if_bridge_tx(*, w3, tx, logs, tx_summary, api_url, api_key, account_address, logger):
    if not tx['to']:
        return False
    account_address_checksum = w3.to_checksum_address(account_address)
    if (
            (
                    (is_account_address(w3, tx['from']) or is_account_address(w3, tx['to'])) and
                    (w3.eth.get_transaction_count(w3.to_checksum_address(tx['from'])) > MAX_NONCE_PLATFORM_WALLET
                     or w3.eth.get_transaction_count(w3.to_checksum_address(tx['to'])) > MAX_NONCE_PLATFORM_WALLET) and
                    not logs
                    and tx['input'] == '0x'
            )
            or
            (len(logs) > 1 and len(tx_summary) == 1 and len(tx_summary.keys()) == 1 and
             next((inner_dict['amount'] > 0 for inner_dict in list(tx_summary.values())), False))
    ):
        return True
    elif ((
          internal_txs := get_internal_txs_by_hash(api_url=api_url, api_key=api_key, tx_hash=tx['hash'], logger=logger))
          and not tx_summary):
        internal_from_addresses = {w3.to_checksum_address(internal_tx['from']) for internal_tx in internal_txs if
                                   internal_tx['from']}
        internal_to_addresses = {w3.to_checksum_address(internal_tx['to']) for internal_tx in internal_txs if
                                 internal_tx['to']}

        return (
                (w3.to_checksum_address(tx['from']) != account_address_checksum and
                 w3.to_checksum_address(tx['to']) != account_address_checksum and
                 account_address_checksum in internal_to_addresses
                 )
                or (
                        w3.to_checksum_address(tx['from']) == account_address_checksum and
                        not is_account_address(w3, tx['to']) and
                        w3.to_checksum_address(tx['to']) in internal_from_addresses and
                        account_address_checksum not in internal_to_addresses and
                        next((int(internal_tx['value']) > 0 for internal_tx in internal_txs if
                              w3.to_checksum_address(tx['to']) == w3.to_checksum_address(internal_tx['from'])), False)
                )
        )
