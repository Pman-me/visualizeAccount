from sqlite3 import OperationalError

from sqlalchemy import create_engine

from src.app.settings import RDBMS_ENGINE


def get_db_engine():
    try:
        return create_engine(RDBMS_ENGINE)
    except OperationalError as err:
        print("***", err)
