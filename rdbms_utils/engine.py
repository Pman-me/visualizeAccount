from sqlite3 import OperationalError

from sqlalchemy import create_engine

from settings.env_settings import EnvSettings


def get_db_engine():
    try:
        return create_engine(EnvSettings().DATABASE_URL)
    except OperationalError as err:
        pass
