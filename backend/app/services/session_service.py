"""
Session Service.

Gerenciamento de sessões de usuário no Redis.
"""

import json
import uuid
from datetime import UTC, datetime, timedelta

from redis.asyncio import Redis


class SessionService:
    """Serviço para gerenciamento de sessões no Redis."""

    SESSION_TTL_DAYS = 7  # Igual ao refresh token

    def __init__(self, redis: Redis) -> None:
        """
        Inicializar o serviço de sessão.

        Args:
            redis: Instância Redis conectada.
        """
        self.redis = redis

    def _get_key(self, user_id: str, session_id: str) -> str:
        """
        Gerar chave de sessão no Redis.

        Args:
            user_id: ID do usuário.
            session_id: ID da sessão.

        Returns:
            Chave formatada para o Redis.
        """
        return f"session:{user_id}:{session_id}"

    async def create_session(
        self,
        user_id: str,
        device_info: dict | None = None,
    ) -> str:
        """
        Criar nova sessão para o usuário.

        Args:
            user_id: UUID do usuário como string.
            device_info: Informações do dispositivo (user_agent, ip, etc).

        Returns:
            ID da sessão criada.
        """
        session_id = str(uuid.uuid4())
        key = self._get_key(user_id, session_id)

        data = {
            "user_id": user_id,
            "session_id": session_id,
            "device_info": device_info or {},
            "created_at": datetime.now(UTC).isoformat(),
        }

        await self.redis.setex(
            key,
            timedelta(days=self.SESSION_TTL_DAYS),
            json.dumps(data),
        )

        return session_id

    async def session_exists(self, user_id: str, session_id: str) -> bool:
        """
        Verificar se uma sessão existe.

        Args:
            user_id: UUID do usuário.
            session_id: ID da sessão.

        Returns:
            True se a sessão existe, False caso contrário.
        """
        key = self._get_key(user_id, session_id)
        return await self.redis.exists(key) > 0

    async def get_session(self, user_id: str, session_id: str) -> dict | None:
        """
        Obter dados de uma sessão.

        Args:
            user_id: UUID do usuário.
            session_id: ID da sessão.

        Returns:
            Dados da sessão ou None se não existir.
        """
        key = self._get_key(user_id, session_id)
        data = await self.redis.get(key)
        if data:
            return json.loads(data)
        return None

    async def invalidate_session(self, user_id: str, session_id: str) -> bool:
        """
        Invalidar uma sessão específica.

        Args:
            user_id: UUID do usuário.
            session_id: ID da sessão.

        Returns:
            True se a sessão foi removida, False se não existia.
        """
        key = self._get_key(user_id, session_id)
        return await self.redis.delete(key) > 0

    async def invalidate_all_sessions(self, user_id: str) -> int:
        """
        Invalidar todas as sessões de um usuário.

        Args:
            user_id: UUID do usuário.

        Returns:
            Número de sessões invalidadas.
        """
        pattern = f"session:{user_id}:*"
        count = 0

        # Usar SCAN para encontrar todas as chaves
        async for key in self.redis.scan_iter(match=pattern):
            await self.redis.delete(key)
            count += 1

        return count

    async def refresh_session(self, user_id: str, session_id: str) -> bool:
        """
        Renovar TTL de uma sessão existente.

        Args:
            user_id: UUID do usuário.
            session_id: ID da sessão.

        Returns:
            True se renovou, False se sessão não existe.
        """
        key = self._get_key(user_id, session_id)
        if await self.redis.exists(key):
            await self.redis.expire(key, timedelta(days=self.SESSION_TTL_DAYS))
            return True
        return False
