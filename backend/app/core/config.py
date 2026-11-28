"""Configuracion de la aplicacion. Todo viene de variables de entorno (o del archivo .env)."""
from functools import lru_cache

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Sin valor por defecto a proposito: si faltan, la app no arranca (no hay secretos en el codigo).
    database_url: str
    secret_key: str
    access_token_expire_minutes: int = 60
    jwt_algorithm: str = "HS256"
    cors_origins: str = "http://localhost:5173"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @field_validator("database_url")
    @classmethod
    def _driver_explicito(cls, url: str) -> str:
        # Segun la version de SQLAlchemy, "postgresql://" apunta a psycopg2 o a psycopg 3.
        # Fijamos psycopg2 (el que instala requirements.txt) para que funcione igual en todos los equipos.
        if url.startswith("postgresql://"):
            return "postgresql+psycopg2://" + url[len("postgresql://"):]
        if url.startswith("postgres://"):
            return "postgresql+psycopg2://" + url[len("postgres://"):]
        return url

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
