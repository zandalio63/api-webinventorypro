"""
Módulo de gestión de conexiones a PostgreSQL utilizando asyncpg.

Proporciona una clase `DBManagement` que maneja un pool de conexiones
asíncronas, permitiendo conectarse, desconectarse y obtener conexiones
de manera segura mediante un context manager.
"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator, Optional

import asyncpg

from core.config import settings


class DBManagement:
    """Gestor asincrónico de conexiones a PostgreSQL."""

    def __init__(self) -> None:
        self.pool: Optional[asyncpg.Pool] = None

    async def connect_to_db(self) -> None:
        """Crea el pool de conexiones a PostgreSQL."""
        self.pool = await asyncpg.create_pool(
            settings.database_url,
            min_size=1,
            max_size=5,
        )
        print("Conectado a PostgreSQL")

    async def disconnect_from_db(self) -> None:
        """Cierra el pool de conexiones a PostgreSQL."""
        if self.pool:
            await self.pool.close()
            print("Conexión a PostgreSQL cerrada")

    @asynccontextmanager
    async def get_connection(self) -> AsyncGenerator[asyncpg.Connection, None]:
        """Obtiene una conexión del pool como context manager."""
        if self.pool is None:
            raise RuntimeError("Pool de conexiones no inicializado")

        conn = await self.pool.acquire()
        try:
            yield conn
        finally:
            await self.pool.release(conn)


db_management = DBManagement()
