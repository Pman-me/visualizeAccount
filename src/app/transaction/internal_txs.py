import json
from json import JSONDecodeError

import requests

from src.app.common.check_response_status import check_response_status


def get_internal_txs_by_hash(*, api_url: str, api_key: str, tx_hash: str, logger):
    try:
        internal_txs_endpoint = f"{api_url}&module=account&action=txlistinternal&txhash={tx_hash}&apikey={api_key}"
        res = json.loads(requests.get(internal_txs_endpoint).text)
        if check_response_status(res):
            return res['result']
        return None
    except (requests.exceptions.RequestException, JSONDecodeError) as err:
        logger.error("An error occurred: %s", err)
