"""
Email Service.

Serviço para envio de emails usando FastAPI-Mail.
"""

import os
from pathlib import Path
from typing import Any

from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from pydantic import EmailStr

from app.config.email import email_settings


class EmailService:
    """Serviço de envio de emails."""

    def __init__(self):
        """Inicializar configuração de email."""
        self.config = ConnectionConfig(
            MAIL_USERNAME=email_settings.smtp_user,
            MAIL_PASSWORD=email_settings.smtp_password,
            MAIL_FROM=email_settings.from_email,
            MAIL_PORT=email_settings.smtp_port,
            MAIL_SERVER=email_settings.smtp_host,
            MAIL_FROM_NAME=email_settings.from_name,
            MAIL_STARTTLS=email_settings.smtp_tls,
            MAIL_SSL_TLS=not email_settings.smtp_tls,
            USE_CREDENTIALS=True,
            VALIDATE_CERTS=True,
        )
        self.fastmail = FastMail(self.config)

    async def send_password_reset_email(
        self,
        to_email: str,
        reset_url: str,
        user_name: str | None = None,
    ) -> None:
        """
        Enviar email de reset de senha.

        Args:
            to_email: Email do destinatário
            reset_url: URL completa para reset de senha
            user_name: Nome do usuário (opcional)
        """
        # Template HTML inline (pode ser movido para arquivo depois)
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Redefinir Senha - Dona Maria IA</title>
            <style>
                body {{ font-family: 'Inter', Arial, sans-serif; background-color: #f5f5f5; margin: 0; padding: 20px; }}
                .container {{ max-width: 600px; margin: 0 auto; background: #ffffff; border-radius: 8px; padding: 40px; }}
                .logo {{ text-align: center; margin-bottom: 30px; }}
                .logo h1 {{ color: #333333; font-size: 24px; }}
                .content {{ color: #333333; line-height: 1.6; }}
                .button {{ display: inline-block; background-color: #aeffde; color: #333333; padding: 14px 28px; text-decoration: none; border-radius: 6px; font-weight: 600; margin: 20px 0; }}
                .button:hover {{ background-color: #9ee8c9; }}
                .footer {{ margin-top: 40px; padding-top: 20px; border-top: 1px solid #e0e0e0; color: #666666; font-size: 12px; }}
                .warning {{ background-color: #fff3cd; padding: 12px; border-radius: 4px; margin: 20px 0; font-size: 14px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="logo">
                    <h1>🏠 Dona Maria IA</h1>
                </div>
                <div class="content">
                    <p>Olá, {user_name or "Usuário"}!</p>
                    <p>Recebemos uma solicitação para redefinir a senha da sua conta. Se você não fez essa solicitação, pode ignorar este email.</p>
                    <p>Para redefinir sua senha, clique no botão abaixo:</p>
                    <p style="text-align: center;">
                        <a href="{reset_url}" class="button">Redefinir Minha Senha</a>
                    </p>
                    <div class="warning">
                        ⚠️ Este link expira em <strong>1 hora</strong>. Após isso, você precisará solicitar um novo link.
                    </div>
                    <p>Se o botão não funcionar, copie e cole o link abaixo no seu navegador:</p>
                    <p style="word-break: break-all; font-size: 12px; color: #666;">{reset_url}</p>
                </div>
                <div class="footer">
                    <p>Este email foi enviado automaticamente. Por favor, não responda.</p>
                    <p>&copy; 2026 Dona Maria IA - A IA que só conta a verdade.</p>
                </div>
            </div>
        </body>
        </html>
        """

        message = MessageSchema(
            subject="Redefinir Senha - Dona Maria IA",
            recipients=[to_email],
            body=html_content,
            subtype=MessageType.html,
        )

        await self.fastmail.send_message(message)