"""
Authentication Schemas.

Schemas Pydantic para autenticação e validação de dados de usuário.
"""

from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class OAuthProvider(str, Enum):
    """Provedores OAuth suportados."""

    GOOGLE = "google"
    GITHUB = "github"


class UserCreate(BaseModel):
    """Schema para criação de novo usuário."""

    email: EmailStr = Field(..., description="Email válido do usuário")
    password: str = Field(
        ..., min_length=8, description="Senha com mínimo 8 caracteres"
    )


class UserResponse(BaseModel):
    """Schema de resposta com dados do usuário."""

    id: UUID
    email: str
    display_name: str | None = None
    auth_provider: str
    created_at: datetime

    model_config = {"from_attributes": True}


class Token(BaseModel):
    """Schema de resposta com tokens JWT."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Schema com dados extraídos do token JWT."""

    user_id: UUID | None = None


class UserLogin(BaseModel):
    """Schema para login de usuário."""

    email: EmailStr = Field(..., description="Email do usuário")
    password: str = Field(..., min_length=1, description="Senha do usuário")


class RefreshTokenRequest(BaseModel):
    """Schema para renovação de token."""

    refresh_token: str = Field(..., description="Refresh token válido")


class OAuthUserInfo(BaseModel):
    """Informações do usuário retornadas pelo provedor OAuth."""

    provider: OAuthProvider
    provider_user_id: str
    email: str
    name: str | None = None
    avatar_url: str | None = None


class OAuthCallbackResponse(BaseModel):
    """Resposta do callback OAuth."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserResponse
