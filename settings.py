from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env')
    ACCOUNT_ADDRESS: Optional[str]
    BASE_API_KEY: Optional[str]
    SCROLL_API_KEY: Optional[str]
