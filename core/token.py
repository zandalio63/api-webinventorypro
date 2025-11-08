"""
Proporciona funciones para crear y verificar tokens de acceso
utilizando la librería `python-jose`. Los tokens incluyen la
información del usuario (`sub`) y una fecha de expiración.
"""

from datetime import datetime, timedelta, timezone
from typing import Tuple

from jose import jwt, ExpiredSignatureError, JWTError

from core.config import settings

def create_access_token(sub : str) -> Tuple[str, timedelta]:
    """
    Crea un token JWT con la información del usuario.

    Args:
        sub (str): Identificador del sujeto (normalmente el email o ID del usuario).

    Returns:
        Tuple[str, timedelta]: El token generado y el tiempo de expiración.
    """
    to_encode = {"sub" : sub}
    expire_delta = timedelta(minutes=settings.access_token_expire_minutes)
    if expire_delta:
        expire = datetime.now(timezone.utc) + expire_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.access_token_expires_minutes_refresh
        )
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(to_encode, settings.secret_key_jwt, algorithm="HS256")
    return encode_jwt, expire_delta

def verify_token(token : str, credential_exception : Exception) -> str:
    """
    Verifica la validez de un token JWT y retorna el campo 'sub' si es válido.

    Args:
        token (str): Token JWT recibido en la cabecera de autorización.
        credential_exception (Exception): Excepción a lanzar en caso de error.

    Returns:
        str: El valor del campo 'sub' (identificador del usuario autenticado).

    Raises:
        credential_exception: Si el token ha expirado, es inválido o no contiene 'sub'.
    """
    try:
        payload = jwt.decode(token, settings.secret_key_jwt, algorithms=["HS256"])
        sub = payload.get("sub")
        if sub is None:
            raise credential_exception
    except ExpiredSignatureError as exc:
        raise credential_exception from exc
    except JWTError as exc:
        raise credential_exception from exc
    return sub
        