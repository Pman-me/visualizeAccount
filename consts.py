from settings import Settings

settings = Settings()

chain_rpcs = {
    'base': ['https://mainnet.base.org']
}

chain_endpoint_api = {
    'base': ('https://api.basescan.org/api', settings.BASE_API_KEY),
    # 'scroll': ('https://api.scrollscan.com/api', settings.SCROLL_API_KEY),
    # 'polygon': ('', settings.POLYGON_API_KEY)
}

chain_data = [
    {'chain': 'base', 'chain_id': 8453, 'rpc': 'https://mainnet.base.org', 'api_endpoint': 'https://api.basescan.org/api',
     'api_key': settings.BASE_API_KEY},
    {'chain': 'scroll', 'chain_id': 534352, 'rpc': 'https://rpc.scroll.io', 'api_endpoint': 'https://api.scrollscan.com/api',
     'api_key': settings.SCROLL_API_KEY},
]

zero_address = 0x0000000000000000000000000000000000000000

transfer_event_sig_hash = 0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef
deposit_event_sig_hash = 0xe1fffcc4923d04b559f4d29a8bfc6cda04eb5b0d3c460751c2402c5c5cc9109c
withdrawal_event_sig_hash = 0x7fcf532c15f0a6db0bd6d0e038bea71d30d808c7d98cb3bf7268a95bf5081b65
