# app/config.py
from typing import Any, List, Optional
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",               # lokale Entwicklung
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # App
    ENVIRONMENT: str = "development"
    APP_NAME: str = "backend"
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    LOG_LEVEL: str = "info"
    API_PREFIX: str = "/api"

    # CORS
    CORS_ORIGINS: List[str] = []

    # Optional
    DATABASE_URL: Optional[str] = None
    REDIS_URL: Optional[str] = None

    # Secrets (Beispiel)
    SECRET_KEY: str = "change-me"

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors(cls, v: Any) -> List[str]:
        if isinstance(v, str):
            return [s.strip() for s in v.split(",") if s.strip()]
        return v

settings = Settings()
