import os
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

DOTENV = os.path.join(os.path.dirname(__file__), "../.env")


class EnvSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=DOTENV)
    BASE_API_KEY: Optional[str]
    SCROLL_API_KEY: Optional[str]
    LINEA_API_KEY: Optional[str]

