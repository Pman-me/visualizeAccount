from sqlalchemy.orm import sessionmaker

from src.app.rdbms_utils.engine import get_db_engine

db_Session = sessionmaker(autoflush=False, autocommit=False, bind=get_db_engine())
