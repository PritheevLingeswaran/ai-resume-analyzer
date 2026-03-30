from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


ROOT_DIR = Path(__file__).resolve().parents[2]
PROJECT_DIR = ROOT_DIR.parent
DATA_DIR = ROOT_DIR / "data"
UPLOAD_DIR = DATA_DIR / "uploads"


class Settings(BaseSettings):
    app_name: str = "AI Resume Analyzer API"
    app_env: str = "development"
    debug: bool = True
    api_prefix: str = "/api"

    database_url: str = Field(
        default=f"sqlite:///{(DATA_DIR / 'smart_resume_analyzer.db').as_posix()}",
    )
    max_upload_size_mb: int = 5
    allowed_extensions: tuple[str, ...] = ("pdf", "docx")

    openai_api_key: str | None = None
    openai_model: str = "gpt-4.1-mini"
    enable_llm_recommendations: bool = True

    cors_origins: list[str] = ["*"]

    model_config = SettingsConfigDict(
        env_prefix="SRA_",
        env_file=ROOT_DIR / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    return Settings()
