"""
API Dependencies.

Dependencies compartilhadas para autenticação e autorização.
"""

from typing import Annotated
from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_db
from app.config.redis import get_redis
from app.models.user import User
from app.services.auth_service import AuthService, verify_token
from app.services.session_service import SessionService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> User:
    """
    Obter usuário atual a partir do token JWT.

    Args:
        token: Token JWT Bearer.
        db: Sessão do banco de dados.

    Returns:
        Objeto User autenticado.

    Raises:
        HTTPException: Se token inválido ou usuário não encontrado.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais inválidas",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token_data = verify_token(token, token_type="access")
    if token_data is None or token_data.user_id is None:
        raise credentials_exception

    auth_service = AuthService(db)
    user = await auth_service.get_user_by_id(token_data.user_id)
    if user is None:
        raise credentials_exception

    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    """
    Verificar se o usuário atual está ativo.

    Para MVP, todos usuários são considerados ativos.
    Em futuras versões, pode verificar status de banimento, etc.

    Args:
        current_user: Usuário obtido do token.

    Returns:
        Usuário ativo.
    """
    # No futuro, verificar se usuário está banido, suspenso, etc.
    return current_user


async def get_session_service(
    redis: Annotated[Redis, Depends(get_redis)],
) -> SessionService:
    """
    Criar instância do SessionService.

    Args:
        redis: Conexão Redis.

    Returns:
        Instância do SessionService.
    """
    return SessionService(redis)


# Type aliases para injeção de dependência
CurrentUser = Annotated[User, Depends(get_current_user)]
ActiveUser = Annotated[User, Depends(get_current_active_user)]
