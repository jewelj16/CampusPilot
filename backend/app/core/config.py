"""
Application configuration.

Phase 1 note: there is no real database or auth provider yet — the mess
module runs entirely on an in-memory repository (see
app/repositories/mess_repository.py) and a hardcoded "current student"
(see app/core/dummy_auth.py). CORS_ORIGINS and APP_ENV are the only knobs
that actually matter right now; the rest are placeholders that match the
shape config will take once M1 (auth) and M2's real Postgres-backed
repository land, so the migration later is a swap, not a rewrite.
"""
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_env: str = "development"
    app_name: str = "CampusPilot API"
    api_v1_prefix: str = "/api/v1"

    # Comma-separated list of allowed origins for the frontend dev server.
    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173"

    # Placeholders for future milestones (M1 auth, M2 real DB) — unused in Phase 1.
    database_url: str | None = None
    jwt_secret: str | None = None

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
