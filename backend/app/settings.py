from pydantic_settings import BaseSettings
from functools import lru_cache


class DatabaseSettings(BaseSettings):
    PGHOST: str
    PGDATABASE: str
    PGUSER: str
    PGPASSWORD: str
    PGPORT: int = 5432

    @property
    def DATABASE_URL(self) -> str:
        url = (
            f'postgresql+asyncpg://{self.PGUSER}:{self.PGPASSWORD}@'
            f'{self.PGHOST}/{self.PGDATABASE}?sslmode=require&channel_binding=require'
        )
        return url


class Settings(DatabaseSettings):
    DEBUG: bool = False


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()