from sqlite3 import OperationalError

from sqlalchemy import create_engine

from common.settings import Settings


def get_db_engine():
    try:
        return create_engine(Settings().DATABASE_URL)
    except OperationalError as err:
        pass
