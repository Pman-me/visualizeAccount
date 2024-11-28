from rdbms_utils.sql_base import SQLBASE


def create_tables(db_engine):
    import models.transaction_model
    SQLBASE.metadata.create_all(db_engine)
