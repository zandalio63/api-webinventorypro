import asyncpg
from typing import Optional, AsyncGenerator
from core.config import settings
from contextlib import asynccontextmanager

class DBManagement :
    def __init__(self):
        self.pool: Optional[asyncpg.Pool] = None
    
    async def connect_to_db(self):
        self.pool = await asyncpg.create_pool(settings.database_url, min_size=1, max_size=5)
        print("Conectado a PostgreSQL")

    async def disconnect_from_db(self):
        if self.pool:
            await self.pool.close()
            print("Conexion a PostgreSQL cerrada")
    
    @asynccontextmanager
    async def get_connection(self) -> AsyncGenerator[asyncpg.Connection, None] :
        """
        Retorna una conexión del pool como context manager.
        """
        if self.pool is None:
            raise RuntimeError("Pool de conexiones no inicializado")
        conn = await self.pool.acquire()
        try:
            yield conn
        finally:
            await self.pool.release(conn)

db_management = DBManagement()