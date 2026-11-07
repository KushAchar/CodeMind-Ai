"""Application settings loaded from environment variables."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime configuration for the FastAPI application."""

    app_name: str = "CodeMind AI"
    app_description: str = "AI-powered Codebase Understanding & Developer Assistant"
    app_version: str = "1.0.0"
    database_url: str = (
        "postgresql+psycopg://codemind:codemind@localhost:5432/codemind_db"
    )
    qdrant_url: str = "http://localhost:6333"
    groq_api_key: str | None = None
    groq_model: str = "llama-3.1-8b-instant"
    github_api_url: str = "https://api.github.com"
    github_token: str | None = None
    github_timeout_seconds: float = 10.0
    cors_origins: list[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
    ]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """Return one cached settings instance for the process."""
    return Settings()
