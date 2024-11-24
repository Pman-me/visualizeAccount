from common.consts import chain_data
from rdbms_utils.create_db import create_db
from rdbms_utils.engine import get_db_engine
from transaction.analyze_transaction_type import categorize_transaction
from transaction.txs_data_per_chain import fetch_txs_per_chain


def main():
    create_db(get_db_engine())
    categorize_transaction(chain_data, fetch_txs_per_chain())


if __name__ == '__main__':
    main()
