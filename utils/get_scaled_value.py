from settings.si import SCALE


def get_eth_scaled_value(amount):
    return f"{float(amount) / SCALE} ETH"
