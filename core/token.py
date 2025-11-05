from jose import jwt, ExpiredSignatureError, JWTError
from datetime import datetime, timedelta, timezone
from typing import Tuple

from .config import settings

def create_access_token(sub : str) -> Tuple[str, timedelta]:
    """
    Crea un JWT y retorna el token junto con el tiempo de expiración.
    """
    to_encode = {"sub" : sub}
    expire_delta = timedelta(minutes=settings.access_token_expire_minutes)
    if expire_delta:
        expire = datetime.now(timezone.utc) + expire_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expires_minutes_refresh)
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(to_encode, settings.secret_key_jwt, algorithm="HS256")
    return encode_jwt, expire_delta

def verify_token(token : str, credential_exception : Exception) -> str:
    """
    Verifica un JWT y retorna el sub (usuario) si es válido.
    Lanza credential_exception si falla la verificación.
    """
    try:
        payload = jwt.decode(token, settings.secret_key_jwt, algorithms=["HS256"])
        sub = payload.get("sub")
        if sub is None:
            raise credential_exception
    except ExpiredSignatureError:
        raise credential_exception
    except JWTError:
        raise credential_exception
    return sub
        