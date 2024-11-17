from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import MappedAsDataclass, DeclarativeBase, sessionmaker

from settings import Settings


class SQLBASE(DeclarativeBase, MappedAsDataclass):
    pass


try:
    engine = create_engine(Settings().DATABASE_URL)
    Session = sessionmaker(autoflush=False, autocommit=False, bind=engine)
except OperationalError as err:
    pass
