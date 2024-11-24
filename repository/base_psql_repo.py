from sqlalchemy.orm import Session

from rdbms_utils.sesstion import get_db_session
from repository.base_repo import BaseRepo


class BasePSQLRepo(BaseRepo):
    def __init__(self, session: Session = get_db_session()):
        self.session = session
