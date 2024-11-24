from rdbms_utils.engine import get_db_engine
from rdbms_utils.sql_base import SQLBASE


def create_tables(db_engine):
    import models.transaction_model
    SQLBASE.metadata.create_all(db_engine)


if __name__ == '__main__':
    create_tables(get_db_engine())
