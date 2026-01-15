"""
Authentication API Router.

Endpoints para registro e autenticação de usuários.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_db
from app.schemas.auth import Token, UserCreate
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db),
) -> Token:
    """
    Registrar novo usuário com email e senha.

    Args:
        user_data: Dados de registro (email e senha).
        db: Sessão do banco de dados.

    Returns:
        Token: Tokens JWT de acesso e refresh.

    Raises:
        HTTPException: Se email já estiver cadastrado.
    """
    auth_service = AuthService(db)

    # Verificar se email já existe
    existing_user = await auth_service.get_user_by_email(user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já cadastrado",
        )

    # Criar usuário
    user = await auth_service.create_user(user_data)

    # Gerar tokens
    tokens = auth_service.create_tokens(user.id)

    return Token(**tokens)
