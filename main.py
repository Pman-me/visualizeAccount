from common.consts import chain_data
from transaction.analyze_transaction_type import categorize_transaction
from transaction.txs_data_per_chain import fetch_txs_per_chain


def main():

    categorize_transaction(chain_data, fetch_txs_per_chain())


if __name__ == '__main__':
    main()
