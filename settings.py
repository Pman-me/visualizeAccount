from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env')
    DATABASE_URL: Optional[str]
    BASE_API_KEY: Optional[str]
    SCROLL_API_KEY: Optional[str]
    REDIS_HOST: Optional[str]
    REDIS_PORT: Optional[str]
    REDIS_PASS: Optional[str]
    REDIS_DB_NO: Optional[str]
