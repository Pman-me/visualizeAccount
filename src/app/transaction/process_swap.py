from web3 import Web3

from src.app.contract.get_token_detail import get_token_details
from src.app.utils.format_token_amount import format_token_amount


def process_swap_tx(w3: Web3, *, api_url, api_key, tx_summary: dict, logger):
    send = recv = ''

    for token_contract_address, value in tx_summary.items():
        decimals, currency = get_token_details(w3=w3, api_url=api_url, api_key=api_key,
                                               token_contract_address=token_contract_address,
                                               logger=logger)

        if decimals is not None and currency is not None:
            if value.get('from') or value.get('deposit'):
                send += format_token_amount(value['amount'], decimals,
                                            currency) if not send else ', ' + format_token_amount(value['amount'],
                                                                                                   decimals, currency)
            elif value.get('to') or value.get('withdrawal'):
                recv = format_token_amount(value['amount'], decimals, currency)
    return send, recv
