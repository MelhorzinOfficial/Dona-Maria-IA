"""
Testes para reset de senha.
"""

import pytest
from httpx import AsyncClient
from unittest.mock import AsyncMock, patch
from datetime import datetime, timedelta, timezone

from app.models.password_reset import PasswordResetToken
from app.services.password_reset_service import PasswordResetService


class TestForgotPassword:
    async def test_forgot_password_sends_email(self, client: AsyncClient, test_user):
        """Deve enviar email quando usuário existe."""
        with patch('app.services.email_service.EmailService.send_password_reset_email', new_callable=AsyncMock) as mock_send:
            response = await client.post("/api/v1/auth/forgot-password", json={
                "email": test_user.email
            })
            assert response.status_code == 200
            mock_send.assert_called_once()

    async def test_forgot_password_unknown_email(self, client: AsyncClient):
        """Deve retornar sucesso mesmo para email inexistente (segurança)."""
        response = await client.post("/api/v1/auth/forgot-password", json={
            "email": "naoexiste@example.com"
        })
        assert response.status_code == 200
        assert "recuperação" in response.json()["message"]


class TestResetPassword:
    async def test_reset_password_valid_token(self, client: AsyncClient, test_reset_token):
        """Deve atualizar senha com token válido."""
        response = await client.post("/api/v1/auth/reset-password", json={
            "token": test_reset_token.raw_token,
            "new_password": "novaSenha123"
        })
        assert response.status_code == 200

    async def test_reset_password_expired_token(self, client: AsyncClient, expired_reset_token):
        """Deve rejeitar token expirado."""
        response = await client.post("/api/v1/auth/reset-password", json={
            "token": expired_reset_token.raw_token,
            "new_password": "novaSenha123"
        })
        assert response.status_code == 400
        assert "expirado" in response.json()["detail"].lower()

    async def test_reset_password_used_token(self, client: AsyncClient, used_reset_token):
        """Deve rejeitar token já utilizado."""
        response = await client.post("/api/v1/auth/reset-password", json={
            "token": used_reset_token.raw_token,
            "new_password": "novaSenha123"
        })
        assert response.status_code == 400

    async def test_reset_password_invalidates_sessions(self, client: AsyncClient, test_reset_token, db_session):
        """Deve invalidar todas as sessões após reset."""
        # TODO: Implementar quando user_sessions for criado
        pass

    async def test_reset_password_short_password(self, client: AsyncClient, test_reset_token):
        """Deve rejeitar senha curta."""
        response = await client.post("/api/v1/auth/reset-password", json={
            "token": test_reset_token.raw_token,
            "new_password": "123"
        })
        assert response.status_code == 422