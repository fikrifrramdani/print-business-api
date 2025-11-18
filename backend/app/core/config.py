from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    # =====================================
    # App
    # =====================================
    APP_NAME: str = "PrintBusinessAPI"
    APP_ENV: str = "development"
    API_VERSION: str = "v1"

    # =====================================
    # Security
    # =====================================
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 120
    ALGORITHM: str = "HS256"

    # =====================================
    # Database
    # =====================================
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    DATABASE_URL: str

    # =====================================
    # CORS / Optional
    # =====================================
    LOG_LEVEL: str = "INFO"
    ALLOW_ORIGINS: str = ""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache()
def get_settings():
    return Settings()
