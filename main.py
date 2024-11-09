from consts import chain_data
from db import engine, SQLBASE
from settings import Settings
from transaction.analyze_transaction_type import categorize_transaction
from transaction.txs_data_per_chain import fetch_txs_per_chain


def main():

    SQLBASE.metadata.create_all(bind=engine)
    categorize_transaction(chain_data, fetch_txs_per_chain(chain_data, Settings().ACCOUNT_ADDRESS))


if __name__ == '__main__':
    main()
