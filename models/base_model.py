from db import SQLBASE


class BaseModel(SQLBASE):
    __abstract__ = True
