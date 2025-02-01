from src.app.common.tx_enum import TxType
from src.app.contract.get_contract_detail import get_contract_name


def transform_tx_data(*, w3, api_url: str, api_key: str, l1_fee: str, tx: dict, tx_type, account_address,
                      logger,
                      send=None,
                      recv=None):
    return {
        'hash': tx['hash'],
        'wallet': account_address,
        'to_contract_name': '' if tx_type == TxType.TRANSFER.value else get_contract_name(w3=w3, api_url=api_url,
                                                                                          api_key=api_key,
                                                                                          contract_address=tx['to'],
                                                                                          logger=logger),
        'send': send,
        'recv': recv,
        'nonce': '' if tx_type == TxType.TRANSFER.value and recv else tx['nonce'],
        'timeStamp': tx['timeStamp'],
        'fee': f"{w3.from_wei((int(tx['gasUsed']) * int(tx['gasPrice']) + int(l1_fee, 16)), 'ether'):.10f}",
        'chain_id': w3.eth.chain_id,
        'type': tx_type
    }
