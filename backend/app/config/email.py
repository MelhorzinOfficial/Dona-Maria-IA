"""
Email Configuration.

Configurações SMTP para envio de emails.
"""

from pydantic_settings import BaseSettings


class EmailSettings(BaseSettings):
    """Configurações de email SMTP."""

    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_password: str = ""
    smtp_tls: bool = True
    from_email: str = "noreply@donamaria.ai"
    from_name: str = "Dona Maria IA"

    # URL base para links no email
    frontend_url: str = "http://localhost:3000"

    # Token settings
    reset_token_expire_hours: int = 1

    class Config:
        env_prefix = "EMAIL_"


email_settings = EmailSettings()