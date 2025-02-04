from sqlalchemy.orm import MappedAsDataclass, DeclarativeBase


class SQLBASE(DeclarativeBase, MappedAsDataclass):
    pass
