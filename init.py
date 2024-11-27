from rdbms_utils.create_tables import create_tables
from rdbms_utils.engine import get_db_engine

create_tables(get_db_engine())
