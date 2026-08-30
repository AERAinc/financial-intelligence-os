from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application
    APP_NAME: str = "Financial Intelligence OS"
    APP_VERSION: str = "0.1.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    API_V1_PREFIX: str = "/api/v1"

    # Database – temporarily using SQLite so we can continue without psycopg
    # We will switch back to PostgreSQL later
    DATABASE_URL: str = "sqlite:///./fios_dev.db"

    # Security
    SECRET_KEY: str = "change-me-in-production-use-openssl-rand-hex-32"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24

    # Multi-tenant
    DEFAULT_TENANT_SLUG: str = "mkrk"


@lru_cache
def get_settings() -> Settings:
    return Settings()