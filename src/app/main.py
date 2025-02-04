from rdbms_utils.create_db import create_db
from rdbms_utils.engine import get_db_engine
from rdbms_utils.sesstion import get_db_session
from repositories.tx_repo import TxRepo
from settings import account_address
from settings.si import CHAINS, ETHERSCAN_API_BASE_URL, ETHERSCAN_API_KEY
from transaction.fetch_and_process_txs import fetch_and_process_txs
from utils.logger import logger
from utils.validate_address import validate_address


def main():

    validate_address(account_address)
    create_db(get_db_engine())
    fetch_and_process_txs(chains=CHAINS, api_base_url=ETHERSCAN_API_BASE_URL, api_key=ETHERSCAN_API_KEY,
                          account_address=account_address, tx_repo=TxRepo(get_db_session()), logger=logger)


if __name__ == '__main__':
    main()
