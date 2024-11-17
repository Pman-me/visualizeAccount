from db import Session


def get_db_session():
    session = Session()
    try:
        return session
    finally:
        session.close()
