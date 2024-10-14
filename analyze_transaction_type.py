import ast
from pprint import pprint

from web3 import Web3

from check_address_type import is_account_address
from contract_name_abi import get_contract_name_abi


def analyze_transaction_type(chain_data: [], txs: []):
    for tx in txs:
        print(tx)
        tx = ast.literal_eval(tx)

        chain = next((chain for chain in chain_data if chain['chain_id'] == tx['chain_id']), None)

        w3 = Web3(Web3.HTTPProvider(chain['rpc']))
        api_key = chain['api_key']
        api_endpoint = chain['api_endpoint']

        # nft tx type
        if tx['tokenDecimal']:
            if tx['from'] == '0x0000000000000000000000000000000000000000':
                # mint
                pass
            elif tx:
                # transfer
                pass
            else:
                # buy or sell
                pass
        else:
            get_contract_name_abi(w3, tx, api_key=api_key, api_endpoint=api_endpoint)
            # for log in logs:
            #     address = log['address']
            #     value = log['data']
            #     topics = log['topics']
            #     # print(address, 'value: ', int(binascii.hexlify(value).decode('ascii'), 16))
            #     print(topics[0])
