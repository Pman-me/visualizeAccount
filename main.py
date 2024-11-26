from rdbms_utils.create_db import create_db
from rdbms_utils.engine import get_db_engine
from rdbms_utils.sesstion import get_db_session
from repository.tx_repo import TxRepo
from settings.si import AccountAddress, CHAIN_DATA
from transaction.analyze_tx_type import process_tx
from transaction.txs_data_per_chain import fetch_txs_per_chain


def main():
    create_db(get_db_engine())
    tx_repo = TxRepo(session=get_db_session())
    process_tx(CHAIN_DATA, fetch_txs_per_chain(CHAIN_DATA, AccountAddress, tx_repo), AccountAddress, tx_repo)


if __name__ == '__main__':
    main()
