"""
Password Reset Service.

Serviço para gerenciar reset de senha via email.
"""

import secrets
import hashlib
from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.password_reset import PasswordResetToken
from app.models.user import User
from app.services.email_service import EmailService
from app.services.auth_service import AuthService
from app.config.email import email_settings


class PasswordResetService:
    """Serviço de reset de senha."""

    def __init__(self, db: AsyncSession):
        """Inicializar serviço."""
        self.db = db
        self.email_service = EmailService()
        self.auth_service = AuthService(db)

    async def request_reset(self, email: str) -> bool:
        """
        Solicitar reset de senha.

        Retorna True sempre (não revelar se email existe).
        """
        # Buscar usuário
        user = await self.auth_service.get_user_by_email(email)
        if not user:
            return True  # Não revelar que email não existe

        # Gerar token seguro
        token = secrets.token_urlsafe(32)
        token_hash = hashlib.sha256(token.encode()).hexdigest()

        # Calcular expiração
        expires_at = datetime.now(timezone.utc) + timedelta(
            hours=email_settings.reset_token_expire_hours
        )

        # Salvar no banco
        reset_token = PasswordResetToken(
            user_id=user.id,
            token_hash=token_hash,
            expires_at=expires_at
        )
        self.db.add(reset_token)
        await self.db.commit()

        # Enviar email com link
        reset_url = f"{email_settings.frontend_url}/reset-password/{token}"
        await self.email_service.send_password_reset_email(
            to_email=email,
            reset_url=reset_url,
            user_name=user.display_name or "Usuário"
        )

        return True

    async def verify_token(self, token: str) -> PasswordResetToken | None:
        """
        Verificar se token é válido e não expirado.
        """
        token_hash = hashlib.sha256(token.encode()).hexdigest()

        result = await self.db.execute(
            select(PasswordResetToken)
            .where(PasswordResetToken.token_hash == token_hash)
            .where(PasswordResetToken.used_at.is_(None))
            .where(PasswordResetToken.expires_at > datetime.now(timezone.utc))
        )
        return result.scalar_one_or_none()

    async def reset_password(self, token: str, new_password: str) -> bool:
        """
        Resetar a senha do usuário.

        Retorna False se token inválido/expirado.
        """
        reset_token = await self.verify_token(token)
        if not reset_token:
            return False

        # Atualizar senha do usuário
        user = await self.db.get(User, reset_token.user_id)
        if not user:
            return False

        user.password_hash = self.auth_service.hash_password(new_password)

        # Marcar token como usado
        reset_token.used_at = datetime.now(timezone.utc)

        # Invalidar todas as sessões do usuário
        await self.auth_service.invalidate_all_sessions(user.id)

        await self.db.commit()
        return True