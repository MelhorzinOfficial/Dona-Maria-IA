"""
OAuth Configuration Settings.

Configurações para autenticação OAuth com Google e GitHub.
"""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class OAuthSettings(BaseSettings):
    """OAuth settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Google OAuth
    google_client_id: str = ""
    google_client_secret: str = ""
    google_authorize_url: str = "https://accounts.google.com/o/oauth2/v2/auth"
    google_token_url: str = "https://oauth2.googleapis.com/token"
    google_userinfo_url: str = "https://www.googleapis.com/oauth2/v3/userinfo"
    google_scopes: list[str] = ["openid", "email", "profile"]

    # GitHub OAuth
    github_client_id: str = ""
    github_client_secret: str = ""
    github_authorize_url: str = "https://github.com/login/oauth/authorize"
    github_token_url: str = "https://github.com/login/oauth/access_token"
    github_userinfo_url: str = "https://api.github.com/user"
    github_emails_url: str = "https://api.github.com/user/emails"
    github_scopes: list[str] = ["read:user", "user:email"]

    # General OAuth Settings
    oauth_redirect_base: str = "http://localhost:8000"
    frontend_url: str = "http://localhost:3000"
    state_secret: str = "change-me-in-production"

    def get_google_redirect_uri(self) -> str:
        """Get Google OAuth callback redirect URI."""
        return f"{self.oauth_redirect_base}/api/v1/auth/oauth/google/callback"

    def get_github_redirect_uri(self) -> str:
        """Get GitHub OAuth callback redirect URI."""
        return f"{self.oauth_redirect_base}/api/v1/auth/oauth/github/callback"


@lru_cache
def get_oauth_settings() -> OAuthSettings:
    """Get cached OAuth settings instance."""
    return OAuthSettings()


oauth_settings = get_oauth_settings()
