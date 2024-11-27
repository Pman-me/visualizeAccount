import requests


def get_normal_txs_by_address(account_address: str, api_url: str, api_key: str) -> list:
    params = {
        'module': 'account',
        'action': 'txlist',
        'address': account_address,
        'startblock': 0,
        'endblock': 99999999,
        'sort': 'asc',
        'apikey': api_key,
    }
    data = requests.get(api_url, params=params).json()
    if data['status'] == '1':
        return data['result']
    else:
        print(data['message'])
