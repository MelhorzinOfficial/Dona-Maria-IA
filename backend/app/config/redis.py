"""
Redis Configuration.

Conexão assíncrona com Redis para gerenciamento de sessões.
"""

from collections.abc import AsyncGenerator

from redis.asyncio import Redis, from_url

from app.config.settings import settings


async def get_redis() -> AsyncGenerator[Redis, None]:
    """
    Criar conexão assíncrona com Redis.

    Yields:
        Instância Redis conectada.
    """
    redis = await from_url(
        settings.REDIS_URL,
        encoding="utf-8",
        decode_responses=True,
    )
    try:
        yield redis
    finally:
        await redis.aclose()
