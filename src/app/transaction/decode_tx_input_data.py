from web3 import Web3

from src.app.contract.get_contract_detail import resolve_contract_address, get_contract_abi


def decode_tx_input_data(*, w3: Web3, api_key: str, api_url: str,  tx, logger):
    try:
        contract_address = resolve_contract_address(tx['to'], w3)

        if abi := get_contract_abi(api_url=api_url, api_key=api_key, contract_address=contract_address, logger=logger):
            contract = w3.eth.contract(address=w3.to_checksum_address(contract_address), abi=abi)

            # Decode transaction input
            func_sig, func_args = contract.decode_function_input(tx['input'])
            print('function args: ', func_args, tx['hash'])

            for arg_name, arg_value in func_args.items():

                if isinstance(arg_value, list) or isinstance(arg_value, tuple):
                    print('2', arg_value)
                    # hex_args = [arg.hex() for arg in arg_value]
                elif isinstance(arg_value, dict):
                    print('3', arg_value)

            # for i, data_element in enumerate(func_args['data']):
            #     # Extract function selector & arguments
            #     selector = data_element[:4]
            #     args_data = data_element[4:]
            #
            # # Decode function input for this data element
            # func_sig, func_args = contract.decode_function_input(selector + args_data)
            # print('func sig: ', func_sig)
            # print('args: ')
            # for arg_name, arg_value in func_args.itme():
            #     print(f' {arg_name}: {arg_value}')
    except ValueError as e:
        print('value error', tx['hash'])
