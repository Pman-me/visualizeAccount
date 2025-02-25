from sqlalchemy.orm import Session

from src.app.rdbms_utils.sesstion import get_db_session
from src.app.repositories.base_repo import BaseRepo


class BasePSQLRepo(BaseRepo):
    def __init__(self, session: Session = get_db_session()):
        self.session = session
