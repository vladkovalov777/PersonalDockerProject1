from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    DEBUG: bool


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()