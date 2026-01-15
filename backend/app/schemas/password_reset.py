"""
Password Reset Schemas.

Schemas Pydantic para reset de senha.
"""

from pydantic import BaseModel, EmailStr, Field


class ForgotPasswordRequest(BaseModel):
    """Request para solicitar reset de senha."""
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    """Request para resetar senha."""
    token: str = Field(..., min_length=32, description="Token de reset")
    new_password: str = Field(..., min_length=8, description="Nova senha com mínimo 8 caracteres")


class ForgotPasswordResponse(BaseModel):
    """Response para forgot password."""
    message: str