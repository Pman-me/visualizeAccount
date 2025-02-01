from src.app.rdbms_utils.sql_base import SQLBASE


def create_tables(db_engine):
    SQLBASE.metadata.create_all(db_engine)
