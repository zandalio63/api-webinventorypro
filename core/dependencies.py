from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from .token import verify_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "login")

UserType = dict

def get_user_email(email : str) -> Optional[UserType]:
    """
    Retorna un usuario a partir del email.
    Por ahora no implementado, devuelve None.
    """
    pass

def get_current_user(token = Depends(oauth2_scheme))-> UserType:
    """
    Devuelve el usuario actual a partir del token.
    Lanza HTTPException si el token es inválido o el usuario no existe.
    """
    credendial_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate" : "Bearer"},
    )
    
    email = verify_token(token, credendial_exception)
    user = get_user_email(email)
    if user is None:
        raise HTTPException(status_code=404, detail="User not exists!!")
    return user