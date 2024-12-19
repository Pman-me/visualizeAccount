from settings.si import SCALE


def get_eth_scaled_value(amount):
    return f"{float(amount) / SCALE} ETH"


def format_token_amount(amount, decimals, currency):
    return f"{float(amount) / 10 ** decimals} {currency}"
