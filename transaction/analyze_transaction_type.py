from pprint import pprint

from web3 import Web3
from web3.exceptions import ABIFunctionNotFound

from consts import transfer_event_sig_hash, account_address, deposit_event_sig_hash, chain_data, zero_address
from contract.checking_proxy_contract import is_eip1967_proxy
from contract.get_contract_detail import get_contract_abi, get_contract_name
from db.sesstion import get_db_session
from repository.tx_repo import TxRepo
from transaction.internal_txs import get_internal_txs


def save_diagnosed_tx(w3: Web3, *, api_endpoint, api_key, data: dict, tx, l1_fee,tx_repo: TxRepo):
    send = recv = native_currency = native_amount = ""

    for token_contract_address, value in data.items():

        if contract_address := is_eip1967_proxy(w3, token_contract_address):
            impl_contract_address = contract_address
        else:
            impl_contract_address = token_contract_address

        if abi := get_contract_abi(api_key=api_key, api_endpoint=api_endpoint, contract_address=impl_contract_address):

            token_contract = w3.eth.contract(address=w3.to_checksum_address(token_contract_address), abi=abi)
            try:
                amount = float(value['amount']) / 10 ** token_contract.functions.decimals().call()
                currency = token_contract.functions.symbol().call()
            except ABIFunctionNotFound as err:
                print(tx['hash'], data, "ABIFunctionNotFound ***********************")
                continue

            if value.get('from'):
                send += f'{amount} {currency}' if not send else f' {amount} {currency}, '
            elif value.get('to'):
                recv = f'{amount} {currency}'
            elif 'from' not in value and 'to' not in value:
                native_currency = currency
                native_amount = amount

    if native_currency:
        if recv:
            send += f'{native_amount} {native_currency}'
        elif send:

            if internal_txs := get_internal_txs(api_endpoint=api_endpoint, api_key=api_key, tx_hash=tx['hash']):

                if filter(lambda _tx: w3.to_checksum_address(_tx['to']) == w3.to_checksum_address(account_address), internal_txs):
                    recv = f'{native_amount} {native_currency}'

    if send and recv:
        # swap
        pprint({
            'hash': tx['hash'],
            'from': account_address,
            'to_contract_name': get_contract_name(api_key=api_key, api_endpoint=api_endpoint,
                                                  contract_address=tx['to']),
            'call_data': tx['input'],
            'send': send,
            'recv': recv,
            'nonce': tx['nonce'],
            'timestamp': tx['timeStamp'],
            'fee': f"{w3.from_wei((int(tx['gasUsed']) * int(tx['gasPrice']) + int(l1_fee, 16)), 'ether'):.10f}",
            'chain': next((item['chain'] for item in chain_data if item['chain_id'] == w3.eth.chain_id), None)
        })
        # tx_repo.set({
        #     'hash': tx['hash'],
        #     'from': tx['from'],
        #     'to_contract_name': get_contract_name(api_key=api_key, api_endpoint=api_endpoint, contract_address=tx['to']),
        #     'call_data': tx['input'],
        #     'in_amount': in_amount,
        #     'out_amount': out_amount,
        #     'in_currency': in_currency,
        #     'out_currency': out_currency,
        #     'nonce': tx['nonce'],
        #     'timestamp': tx['timeStamp'],
        #     'fee': w3.from_wei(int(tx['gasUsed']) * int(tx['gasPrice']), 'ether'),
        #     'chain': next((item['chain'] for item in chain_data if item['chain_id'] == w3.eth.chain_id), None)
        # })


def categorize_transaction(chain_data: [], txs_per_chain: dict):
    for chain_id, txs in txs_per_chain.items():

        chain = next((chain for chain in chain_data if chain['chain_id'] == chain_id), None)

        w3 = Web3(Web3.HTTPProvider(chain['rpc']))
        api_key = chain['api_key']
        api_endpoint = chain['api_endpoint']

        for tx in txs:
            tx_receipt = w3.eth.get_transaction_receipt(tx['hash'])
            if logs := tx_receipt['logs']:
                # fetch src & dst per token transfer in transaction
                src_dst_per_token_contract = analyze_logs_per_tx(w3, logs)
                # find swap type
                if src_dst_per_token_contract:
                    save_diagnosed_tx(w3, api_endpoint=api_endpoint, api_key=api_key,
                                      data=src_dst_per_token_contract,
                                      tx=tx, l1_fee=tx_receipt['l1Fee'], tx_repo=TxRepo(session=get_db_session()))

                # detect bridge process after determining the approximate type of all transactions

            else:
                pass

            # decode_tx_input_data(w3, tx, api_key=api_key, api_endpoint=api_endpoint)
            # for log in logs:
            #     address = log['address']
            #     value = log['data']
            #     topics = log['topics']
            #     # print(address, 'value: ', int(binascii.hexlify(value).decode('ascii'), 16))
            #     print(topics[0])


def analyze_logs_per_tx(w3: Web3, logs) -> dict:
    src_dst_per_token_contract = {}
    for log in logs:

        amount = int(log['data'].hex(), 16) if log['data'].hex() != '0x' else 0
        event_sig_hash = int(log['topics'][0].hex(), 16)

        if event_sig_hash == transfer_event_sig_hash:

            if w3.to_checksum_address('0x' + log['topics'][1].hex()[-40:]) == w3.to_checksum_address(account_address) and int(log['topics'][2].hex(), 16) != zero_address:
                src_dst_per_token_contract[log['address']] = {'from': True, 'amount': amount}

            if w3.to_checksum_address('0x' + log['topics'][2].hex()[-40:]) == w3.to_checksum_address(account_address) and int(log['topics'][1].hex(), 16) != zero_address:
                src_dst_per_token_contract[log['address']] = {'to': True, 'amount': amount}

        elif event_sig_hash == deposit_event_sig_hash:
            src_dst_per_token_contract[log['address']] = {'amount': amount}

    return src_dst_per_token_contract
