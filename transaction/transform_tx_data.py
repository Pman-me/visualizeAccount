from consts import chain_data
from contract.get_contract_detail import get_contract_name
from tx_enum import TxType


def transform_tx_data(w3, api_endpoint, api_key, *, l1_fee, tx, tx_type: TxType, send=None, recv=None):
    return {
        'hash': tx['hash'],
        'from': tx['from'],
        'to_contract_name': get_contract_name(api_key=api_key, api_endpoint=api_endpoint,
                                              contract_address=tx['to']),
        'send': send,
        'recv': recv,
        'nonce': tx['nonce'],
        'timeStamp': tx['timeStamp'],
        'fee': f"{w3.from_wei((int(tx['gasUsed']) * int(tx['gasPrice']) + int(l1_fee, 16)), 'ether'):.10f}",
        'chain': next((item['chain'] for item in chain_data if item['chain_id'] == w3.eth.chain_id), None),
        'type': tx_type
    }
