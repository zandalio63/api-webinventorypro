"""
Dependencias de seguridad y autenticación para la API.

Este módulo define las funciones relacionadas con la obtención
del usuario autenticado a partir del token JWT, utilizando
FastAPI y el esquema OAuth2.
"""

from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from schemas.user import UserOut, UserFilter
from services.user_service import UserService
from .token import verify_token

# Esquema OAuth2 utilizado para obtener el token de acceso (Bearer)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "login")

async def get_user_email(email: str) -> Optional[UserOut]:
    """
    Obtiene un usuario a partir de su correo electrónico.

    Args:
        email (str): Correo electrónico del usuario.

    Returns:
        Optional[UserOut]: El usuario encontrado o None si no existe.
    """
    users = await UserService.get_users(UserFilter(email=email))
    return users[0] if users else None

async def get_current_user(token = Depends(oauth2_scheme))-> UserOut:
    """
    Retorna el usuario actual autenticado a partir del token JWT.

    Args:
        token (str): Token JWT proporcionado en la cabecera Authorization.

    Returns:
        UserOut: El usuario autenticado correspondiente al token.

    Raises:
        HTTPException: Si el token no es válido o el usuario no existe.
    """
    credendial_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate" : "Bearer"},
    )

    email = verify_token(token, credendial_exception)
    user = await get_user_email(email)
    if user is None:
        raise HTTPException(status_code=404, detail="User not exists!!")
    return user
