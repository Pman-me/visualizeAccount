from sqlalchemy.orm import Session

from db.sesstion import get_db_session
from models.base_model import BaseModel
from repository.base_repo import BaseRepo


class BasePSQLRepo(BaseRepo):
    def __init__(self, session: Session = get_db_session()):
        self.session = session
