from fastapi import APIRouter, HTTPException, status
from werkzeug.security import generate_password_hash, check_password_hash

from schemas.auth import LoginAuth, RegisterAuth, TokenResponse
from schemas.user import UserInsert
from core.dependencies import get_user_email
from core.token import create_access_token
from services.user_service import user_service

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
async def login(login_data: LoginAuth):
    # 1. Buscar usuario por email
    user = await get_user_email(login_data.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Email not found."
        )
    
    # 2. Verificar contraseña
    if not check_password_hash(user.password, login_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid password."
        )

    # 3. Crear token de acceso
    access_token, access_token_expires = create_access_token(user.email)

    # 4. Devolver respuesta
    return {
        "access_token": access_token,
        "token_type": "Bearer",
        "expire": int(access_token_expires.total_seconds())
    }
    
@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(register_data: RegisterAuth):
    # Verificar si el usuario ya existe
    existing_user = await get_user_email(register_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered."
        )
    
    # Hashear contraseña
    hashed_password = generate_password_hash(register_data.password)
    
    # Crear modelo de inserción
    user_insert = UserInsert(
        first_name=register_data.first_name,
        last_name=register_data.last_name,
        email=register_data.email,
        password=hashed_password
    )

    # Insertar usuario en base de datos
    new_id = await user_service.insert_user(user_insert)
    if not new_id:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error registering user."
        )

    # Crear token de acceso
    access_token, access_token_expires = create_access_token(register_data.email)

    # Respuesta final
    return {
        "access_token": access_token,
        "token_type": "Bearer",
        "expire": int(access_token_expires.total_seconds())
    }