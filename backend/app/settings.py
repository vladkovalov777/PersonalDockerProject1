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
            f'{self.PGHOST}/{self.PGDATABASE}'
        )
        return url


class JWTSettings(BaseSettings):
    JWT_SECRET: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_LIFETIME_MINUTES: int = 15
    REFRESH_TOKEN_LIFETIME_MINUTES: int = 60


class Settings(DatabaseSettings, JWTSettings):
    DEBUG: bool = False


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()