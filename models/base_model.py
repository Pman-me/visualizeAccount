from rdbms_utils.sql_base import SQLBASE


class BaseModel(SQLBASE):
    __abstract__ = True
