import requests


def get_performed_txs_by_address(account_address: str, api_base_url: str, api_key: str, chain_id) -> list:
    params = {
        'chainid': chain_id,
        'module': 'account',
        'action': 'txlist',
        'address': account_address,
        'startblock': 0,
        'endblock': 99999999,
        'sort': 'asc',
        'apikey': api_key,
    }
    data = requests.get(api_base_url, params=params).json()
    if data['status'] == '1':
        return data['result']
    else:
        print(data['message'])
