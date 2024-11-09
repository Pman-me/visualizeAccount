import json

import requests

from check_response_status import check_response_status


def get_internal_txs_by_hash(*, api_endpoint: str, api_key: str, tx_hash: str):
    try:
        internal_txs_endpoint = f"{api_endpoint}?module=account&action=txlistinternal&txhash={tx_hash}&apikey={api_key}"
        res = json.loads(requests.get(internal_txs_endpoint).text)
        if check_response_status(res):
            return res['result']
        return None
    except requests.exceptions.RequestException as e:
        pass