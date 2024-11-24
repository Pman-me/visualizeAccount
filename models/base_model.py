from rdbms_utils import SQLBASE


class BaseModel(SQLBASE):
    __abstract__ = True
