from fastapi import APIRouter, HTTPException, status, Depends
from werkzeug.security import generate_password_hash, check_password_hash

from schemas.auth import TokenResponse
from schemas.user import ProfileUpdate, UserUpdate, UserOut
from core.dependencies import get_current_user, get_user_email
from core.token import create_access_token
from services.user_service import user_service

router = APIRouter(prefix="/profile", tags=["Profile"])

@router.put('/me', response_model=TokenResponse, status_code=status.HTTP_200_OK)
async def profile_update(user_data : ProfileUpdate, current_user : UserOut= Depends(get_current_user)):
    # Validar si se quiere actualizar el email
    if user_data.email and (user_data.email != current_user.email):
        # Validar que el email no exista
        email_exists = await get_user_email(email=user_data.email)
        if email_exists:
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered."
        )
    
    # Validar que se quiere actualizar la password
    if user_data.password:
        # Validar que la password es la correcta
        check_password = check_password_hash(current_user.password, user_data.password)
        if not check_password:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Old password is incorrect!!")
        user_data.new_password = generate_password_hash(user_data.new_password)
    
    # Esquema que recibira el servicio actualizar
    password_updated = user_data.password or current_user.password 
    email_updated= user_data.email or current_user.email
    user_update = UserUpdate(first_name=user_data.first_name, last_name=user_data.last_name, email=email_updated, id=current_user.id, password=password_updated)
    
    # Actualizar usuario en base de datos
    updated = await user_service.update_user(user_update) 
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updated user."
        )

    # Crear token de acceso
    access_token, access_token_expires = create_access_token(email_updated)

    # Respuesta final
    return {
        "access_token": access_token,
        "token_type": "Bearer",
        "expire": int(access_token_expires.total_seconds())
    }