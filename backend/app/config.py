from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "USV Events API"
    debug: bool = False

    database_url: str = "sqlite:///./data/app.db"

    jwt_secret: str = "change-me-in-production-use-long-random-string"
    jwt_algorithm: str = "HS256"
    jwt_expires_minutes: int = 60 * 24

    google_client_id: str = ""
    student_email_suffix: str = "@student.usv.ro"

    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173"

    bootstrap_admin_email: str = "admin@local.test"
    bootstrap_admin_password: str = ""


@lru_cache
def get_settings() -> Settings:
    return Settings()
