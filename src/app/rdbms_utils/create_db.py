from src.app.rdbms_utils.create_tables import create_tables


def create_db(db_engine):
    create_tables(db_engine)
