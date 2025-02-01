from src.app.rdbms_utils.session_handler import db_Session


def get_db_session():
    session = db_Session()
    try:
        return session
    finally:
        session.close()
