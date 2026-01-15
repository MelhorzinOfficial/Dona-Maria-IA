"""
Authentication Service.

Fornece funções para hash/verificação de senha e criação/verificação de tokens JWT.
"""

from datetime import UTC, datetime, timedelta
from uuid import UUID

import bcrypt
from jose import JWTError, jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.auth import auth_settings
from app.models.user import User
from app.schemas.auth import TokenData, UserCreate


def hash_password(password: str) -> str:
    """
    Hash uma senha usando bcrypt com cost factor configurado.

    Args:
        password: Senha em texto plano.

    Returns:
        Hash bcrypt da senha.
    """
    password_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt(rounds=auth_settings.BCRYPT_ROUNDS)
    return bcrypt.hashpw(password_bytes, salt).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verificar se uma senha corresponde ao hash.

    Args:
        plain_password: Senha em texto plano.
        hashed_password: Hash bcrypt armazenado.

    Returns:
        True se a senha corresponder, False caso contrário.
    """
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )


def create_access_token(user_id: UUID) -> str:
    """
    Criar um token JWT de acesso.

    Args:
        user_id: UUID do usuário.

    Returns:
        Token JWT codificado.
    """
    expire = datetime.now(UTC) + timedelta(
        minutes=auth_settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode = {"sub": str(user_id), "exp": expire, "type": "access"}
    return jwt.encode(
        to_encode, auth_settings.SECRET_KEY, algorithm=auth_settings.ALGORITHM
    )


def create_refresh_token(user_id: UUID) -> str:
    """
    Criar um token JWT de refresh.

    Args:
        user_id: UUID do usuário.

    Returns:
        Token JWT codificado.
    """
    expire = datetime.now(UTC) + timedelta(days=auth_settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode = {"sub": str(user_id), "exp": expire, "type": "refresh"}
    return jwt.encode(
        to_encode, auth_settings.SECRET_KEY, algorithm=auth_settings.ALGORITHM
    )


def verify_token(token: str, token_type: str = "access") -> TokenData | None:
    """
    Verificar e decodificar um token JWT.

    Args:
        token: Token JWT a ser verificado.
        token_type: Tipo esperado do token ("access" ou "refresh").

    Returns:
        TokenData com user_id se válido, None caso contrário.
    """
    try:
        payload = jwt.decode(
            token, auth_settings.SECRET_KEY, algorithms=[auth_settings.ALGORITHM]
        )
        user_id: str | None = payload.get("sub")
        payload_type: str | None = payload.get("type")

        if user_id is None or payload_type != token_type:
            return None

        return TokenData(user_id=UUID(user_id))
    except JWTError:
        return None


class AuthService:
    """Serviço de autenticação com operações de banco de dados."""

    def __init__(self, db: AsyncSession) -> None:
        """
        Inicializar o serviço de autenticação.

        Args:
            db: Sessão assíncrona do SQLAlchemy.
        """
        self.db = db

    async def get_user_by_email(self, email: str) -> User | None:
        """
        Buscar usuário por email.

        Args:
            email: Email do usuário.

        Returns:
            Objeto User se encontrado, None caso contrário.
        """
        stmt = select(User).where(User.email == email.lower())
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_user_by_id(self, user_id: UUID) -> User | None:
        """
        Buscar usuário por ID.

        Args:
            user_id: UUID do usuário.

        Returns:
            Objeto User se encontrado, None caso contrário.
        """
        stmt = select(User).where(User.id == user_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def create_user(self, user_data: UserCreate) -> User:
        """
        Criar novo usuário no banco de dados.

        Args:
            user_data: Dados de criação do usuário (email, password).

        Returns:
            Objeto User criado.
        """
        user = User(
            email=user_data.email.lower(),
            password_hash=hash_password(user_data.password),
            auth_provider="email",
        )
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    def create_tokens(self, user_id: UUID) -> dict[str, str]:
        """
        Criar par de tokens (access e refresh) para um usuário.

        Args:
            user_id: UUID do usuário.

        Returns:
            Dicionário com access_token, refresh_token e token_type.
        """
        return {
            "access_token": create_access_token(user_id),
            "refresh_token": create_refresh_token(user_id),
            "token_type": "bearer",
        }
