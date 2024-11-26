from settings.si import DEV_ENV

if DEV_ENV:
    from .local_setting import *
else:
    from .si import *

RDBMS_ENGINE = f"postgresql://{RDBMS_USER}:{RDBMS_PASSWORD}@{RDBMS_HOST}:{RDBMS_PORT}/{RDBMS_DB}"
