from contract.get_contract_detail import get_contract_name
from common.tx_enum import TxType


def transform_tx_data(w3, api_url: str, api_key: str, *, l1_fee: str, tx: dict, tx_type: TxType, chain_data, send=None,
                      recv=None):
    return {
        'hash': tx['hash'],
        'wallet': tx['from'],
        'to_contract_name': get_contract_name(api_url=api_url, api_key=api_key, contract_address=tx['to']),
        'send': send,
        'recv': recv,
        'nonce': tx['nonce'],
        'timeStamp': tx['timeStamp'],
        'fee': f"{w3.from_wei((int(tx['gasUsed']) * int(tx['gasPrice']) + int(l1_fee, 16)), 'ether'):.10f}",
        'chain': next((item['chain'] for item in chain_data if item['chain_id'] == w3.eth.chain_id), None),
        'type': tx_type
    }
