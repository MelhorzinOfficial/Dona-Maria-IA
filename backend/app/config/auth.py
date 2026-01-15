"""
Authentication Configuration Settings.

Configurações de JWT e autenticação carregadas de variáveis de ambiente.
"""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class AuthSettings(BaseSettings):
    """Authentication settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_prefix="AUTH_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    # JWT Configuration
    SECRET_KEY: str = "your-super-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Password Hashing
    BCRYPT_ROUNDS: int = 12


@lru_cache
def get_auth_settings() -> AuthSettings:
    """Get cached auth settings instance."""
    return AuthSettings()


auth_settings = get_auth_settings()
