from rdbms_utils.create_db import create_db
from rdbms_utils.engine import get_db_engine
from rdbms_utils.sesstion import get_db_session
from repositories.tx_repo import TxRepo
from settings import AccountAddress
from settings.si import CHAIN_DATA
from transaction.fetch_and_process_txs import fetch_and_process_txs
from utils.validate_address import validate_address


def main():
    validate_address(AccountAddress)

    create_db(get_db_engine())
    tx_repo = TxRepo(session=get_db_session())

    fetch_and_process_txs(CHAIN_DATA, AccountAddress, tx_repo)


if __name__ == '__main__':
    main()
