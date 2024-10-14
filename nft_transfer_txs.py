import requests


def get_nft_transfer_txs_by_address(account_address: str, endpoint: str, api_key: str):
    action_map = {
        'erc721': 'tokennfttx',
        'erc1155': 'token1155tx'
    }
    for token_type, action in action_map.items():
        params = {
            'module': 'account',
            'action': action,
            'address': account_address,
            'startblock': 0,
            'endblock': 99999999,
            'sort': 'asc',
            'apikey': api_key
        }
        data = requests.get(endpoint, params=params).json()
        if data['status'] == '1':
            return data['result']
        else:
            print(data['message'])
