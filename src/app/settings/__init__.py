from src.app.settings.si import DEV_ENV

if DEV_ENV:
    from .dev_settings import *

try:
    from .local_settings import *
except ImportError:
    pass

RDBMS_ENGINE = f"postgresql://{RDBMS_USER}:{RDBMS_PASSWORD}@{RDBMS_HOST}:{RDBMS_PORT}/{RDBMS_DB}"
account_address = AccountAddress
