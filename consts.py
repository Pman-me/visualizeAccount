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
