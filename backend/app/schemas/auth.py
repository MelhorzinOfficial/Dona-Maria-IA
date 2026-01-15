"""
Authentication Schemas.

Schemas Pydantic para autenticação e validação de dados de usuário.
"""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


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
