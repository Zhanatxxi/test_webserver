from pathlib import Path
from typing import Any

from pydantic import BaseSettings, validator, PostgresDsn


class AsyncPostgresDsn(PostgresDsn):
    allowed_schemes = list(PostgresDsn.allowed_schemes) + ["postgresql+asyncpg"]


class Settings(BaseSettings):
    """Base settings project"""
    BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
    APP_DIR = BASE_DIR / "src"
    DEBUG: bool

    MEDIA_ROOT = "media"
    MEDIA_PATH = BASE_DIR / "media"
    HOST_NAME: str

    ROUTING_KEY: str = 'save_image'
    PREFETCH_COUNT: int = 10

    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: str
    DB_DATABASE: str
    DB_POOL_SIZE: int = 5
    DB_MAX_OVERFLOW: int = 15
    SQLALCHEMY_DATABASE_URI: AsyncPostgresDsn | None = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: str | None, values: dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return AsyncPostgresDsn.build(
            scheme="postgresql+asyncpg",
            user=values.get("DB_USER"),
            password=values.get("DB_PASSWORD"),
            host=values.get("DB_HOST"),
            port=values.get("DB_PORT"),
            path=f"/{values.get('DB_DATABASE') or ''}",
        )

    class Config:
        env_file = f"{Path(__file__).resolve().parent.parent}/.env"


settings = Settings()
