"""
OAuth Service.

Serviço para autenticação via OAuth (Google e GitHub).
"""

import secrets
from datetime import UTC, datetime, timedelta
from typing import Literal
from urllib.parse import urlencode

import httpx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.oauth import oauth_settings
from app.models.user import User
from app.schemas.auth import OAuthProvider, OAuthUserInfo

OAuthProviderType = Literal["google", "github"]


class OAuthStateStore:
    """
    Armazenamento de state tokens para prevenção de CSRF.

    Em produção, usar Redis para persistência distribuída.
    """

    def __init__(self) -> None:
        self._states: dict[str, datetime] = {}
        self._ttl_minutes: int = 10

    def create_state(self) -> str:
        """
        Criar novo state token.

        Returns:
            Token state seguro.
        """
        state = secrets.token_urlsafe(32)
        self._states[state] = datetime.now(UTC)
        self._cleanup_expired()
        return state

    def validate_state(self, state: str) -> bool:
        """
        Validar state token.

        Args:
            state: Token a ser validado.

        Returns:
            True se válido, False caso contrário.
        """
        if state not in self._states:
            return False

        created_at = self._states.pop(state)
        now = datetime.now(UTC)
        # Ajustar timezone se necessário
        if created_at.tzinfo is None:
            created_at = created_at.replace(tzinfo=UTC)
        return now - created_at < timedelta(minutes=self._ttl_minutes)

    def _cleanup_expired(self) -> None:
        """Remover states expirados."""
        now = datetime.now(UTC)
        expired = [
            state
            for state, created_at in self._states.items()
            if now
            - (
                created_at
                if created_at.tzinfo
                else created_at.replace(tzinfo=UTC)
            )
            > timedelta(minutes=self._ttl_minutes)
        ]
        for state in expired:
            self._states.pop(state, None)


# Instância global do state store
state_store = OAuthStateStore()


class OAuthService:
    """Serviço para autenticação OAuth."""

    def __init__(self, db: AsyncSession) -> None:
        """
        Inicializar o serviço OAuth.

        Args:
            db: Sessão assíncrona do SQLAlchemy.
        """
        self.db = db

    def generate_oauth_url(self, provider: OAuthProviderType) -> tuple[str, str]:
        """
        Gerar URL de autorização OAuth e state token.

        Args:
            provider: Provedor OAuth ('google' ou 'github').

        Returns:
            Tuple de (authorize_url, state).

        Raises:
            ValueError: Se provedor não suportado.
        """
        state = state_store.create_state()

        if provider == "google":
            params = {
                "client_id": oauth_settings.google_client_id,
                "redirect_uri": oauth_settings.get_google_redirect_uri(),
                "response_type": "code",
                "scope": " ".join(oauth_settings.google_scopes),
                "state": state,
                "access_type": "offline",
                "prompt": "consent",
            }
            return f"{oauth_settings.google_authorize_url}?{urlencode(params)}", state

        if provider == "github":
            params = {
                "client_id": oauth_settings.github_client_id,
                "redirect_uri": oauth_settings.get_github_redirect_uri(),
                "scope": " ".join(oauth_settings.github_scopes),
                "state": state,
            }
            return f"{oauth_settings.github_authorize_url}?{urlencode(params)}", state

        raise ValueError(f"Provider não suportado: {provider}")

    def validate_state(self, state: str) -> bool:
        """
        Validar state token para prevenir CSRF.

        Args:
            state: Token state do callback.

        Returns:
            True se válido, False caso contrário.
        """
        return state_store.validate_state(state)

    async def exchange_code_for_token(
        self, provider: OAuthProviderType, code: str
    ) -> str:
        """
        Trocar authorization code por access token.

        Args:
            provider: Provedor OAuth.
            code: Authorization code do callback.

        Returns:
            Access token do provedor.

        Raises:
            httpx.HTTPStatusError: Se requisição falhar.
            ValueError: Se provedor não suportado.
        """
        async with httpx.AsyncClient() as client:
            if provider == "google":
                response = await client.post(
                    oauth_settings.google_token_url,
                    data={
                        "client_id": oauth_settings.google_client_id,
                        "client_secret": oauth_settings.google_client_secret,
                        "code": code,
                        "grant_type": "authorization_code",
                        "redirect_uri": oauth_settings.get_google_redirect_uri(),
                    },
                )
                response.raise_for_status()
                data = response.json()
                return data["access_token"]

            if provider == "github":
                response = await client.post(
                    oauth_settings.github_token_url,
                    data={
                        "client_id": oauth_settings.github_client_id,
                        "client_secret": oauth_settings.github_client_secret,
                        "code": code,
                    },
                    headers={"Accept": "application/json"},
                )
                response.raise_for_status()
                data = response.json()

                if "error" in data:
                    raise httpx.HTTPStatusError(
                        message=data.get("error_description", data["error"]),
                        request=response.request,
                        response=response,
                    )

                return data["access_token"]

            raise ValueError(f"Provider não suportado: {provider}")

    async def get_user_info(
        self, provider: OAuthProviderType, access_token: str
    ) -> OAuthUserInfo:
        """
        Buscar informações do usuário do provedor OAuth.

        Args:
            provider: Provedor OAuth.
            access_token: Token de acesso do provedor.

        Returns:
            Informações do usuário OAuth.

        Raises:
            httpx.HTTPStatusError: Se requisição falhar.
            ValueError: Se provedor não suportado ou email não disponível.
        """
        async with httpx.AsyncClient() as client:
            headers = {"Authorization": f"Bearer {access_token}"}

            if provider == "google":
                response = await client.get(
                    oauth_settings.google_userinfo_url, headers=headers
                )
                response.raise_for_status()
                data = response.json()

                if not data.get("email"):
                    raise ValueError("Email não disponível na conta Google")

                return OAuthUserInfo(
                    provider=OAuthProvider.GOOGLE,
                    provider_user_id=data["sub"],
                    email=data["email"],
                    name=data.get("name"),
                    avatar_url=data.get("picture"),
                )

            if provider == "github":
                # GitHub precisa de duas chamadas: user info + emails
                response = await client.get(
                    oauth_settings.github_userinfo_url, headers=headers
                )
                response.raise_for_status()
                user_data = response.json()

                # Buscar email primário (GitHub pode ter email privado)
                emails_response = await client.get(
                    oauth_settings.github_emails_url, headers=headers
                )
                emails_response.raise_for_status()
                emails = emails_response.json()
                primary_email = next(
                    (e["email"] for e in emails if e.get("primary")), None
                )

                email = primary_email or user_data.get("email")
                if not email:
                    raise ValueError("Email não disponível na conta GitHub")

                return OAuthUserInfo(
                    provider=OAuthProvider.GITHUB,
                    provider_user_id=str(user_data["id"]),
                    email=email,
                    name=user_data.get("name") or user_data.get("login"),
                    avatar_url=user_data.get("avatar_url"),
                )

            raise ValueError(f"Provider não suportado: {provider}")

    async def get_or_create_user(self, user_info: OAuthUserInfo) -> User:
        """
        Buscar usuário existente ou criar novo.

        Se email já existir, vincula automaticamente a conta OAuth.

        Args:
            user_info: Informações do usuário OAuth.

        Returns:
            Objeto User (existente ou novo).
        """
        # Buscar por email existente (case-insensitive)
        stmt = select(User).where(User.email == user_info.email.lower())
        result = await self.db.execute(stmt)
        existing_user = result.scalar_one_or_none()

        if existing_user:
            # Vincular OAuth a conta existente - atualizar dados opcionais
            if not existing_user.avatar_url and user_info.avatar_url:
                existing_user.avatar_url = user_info.avatar_url
            if not existing_user.display_name and user_info.name:
                existing_user.display_name = user_info.name
            await self.db.commit()
            await self.db.refresh(existing_user)
            return existing_user

        # Criar novo usuário OAuth
        new_user = User(
            email=user_info.email.lower(),
            display_name=user_info.name,
            avatar_url=user_info.avatar_url,
            auth_provider=user_info.provider.value,
            password_hash=None,  # OAuth users não têm senha
        )
        self.db.add(new_user)
        await self.db.commit()
        await self.db.refresh(new_user)
        return new_user
