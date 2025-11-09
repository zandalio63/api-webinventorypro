"""
Aplicación FastAPI principal.

Este módulo inicializa la aplicación FastAPI, define su ciclo de vida,
maneja los cors y registra los routers de los distintos módulos de la API.

Routers incluidos:
- auth: Gestión de autenticación (login y registro de usuarios).
- user: Gestión de usuarios y perfil.
- product: Gestión de productos (CRUD y búsquedas).

- CORS:
- origins, methods, credentials, headers

Ciclo de vida de la aplicación:
- Conexión a la base de datos al iniciar la aplicación.
- Desconexión de la base de datos al cerrar la aplicación.

Endpoint principal:
- GET / : Retorna un mensaje de prueba.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routers import auth, product, user
from core.config import settings
from db.connnection import db_management


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """
    Administra el ciclo de vida de la aplicación.

    - Conecta a la base de datos al iniciar la app.
    - Desconecta la base de datos al cerrar la app.

    Args:
        app (FastAPI): Instancia de la aplicación FastAPI.

    Yields:
        None
    """
    await db_management.connect_to_db()
    yield
    await db_management.disconnect_from_db()


# Inicialización de la aplicación FastAPI
app = FastAPI(lifespan=lifespan)

# Configuracion cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins.split(),
    allow_methods=settings.allowed_methods.split(),
    allow_headers=settings.allowed_headers.split(),
    allow_credentials=settings.allowed_credentials
)


# Inclusión de routers
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(product.router)


@app.get("/")
async def main():
    """
    Endpoint principal de prueba.

    Retorna un mensaje simple de bienvenida.

    Returns:
        dict: Contiene un mensaje de saludo.
    """
    return {"hello": "World"}
