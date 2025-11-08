"""
Módulo de rutas para la gestión del perfil de usuario.

Este módulo define los endpoints de la API relacionados con el perfil del usuario, incluyendo:
- Consulta de la información del perfil del usuario actual.
- Actualización de los datos del perfil, incluyendo nombre, apellido, email y contraseña.

Cada endpoint requiere autenticación mediante `get_current_user`. 
La actualización de contraseña valida la contraseña actual antes de aplicar los cambios.
"""

from fastapi import APIRouter, HTTPException, status, Depends
from werkzeug.security import generate_password_hash, check_password_hash

from schemas.auth import TokenResponse
from schemas.user import ProfileUpdate, UserUpdate, UserOut, UserBase
from core.dependencies import get_current_user, get_user_email
from core.token import create_access_token
from services.user_service import user_service

router = APIRouter(prefix="/profile", tags=["Profile"])


@router.put(
    "/me",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK
)
async def profile_update(
    user_data: ProfileUpdate,
    current_user: UserOut = Depends(get_current_user)
):
    """
    Actualiza la información del perfil del usuario actual.

    - Valida si se actualiza el email y que no exista ya en la base de datos.
    - Valida la contraseña actual antes de actualizarla.
    - Genera un nuevo token de acceso tras la actualización.

    Args:
        user_data (ProfileUpdate): Datos a actualizar.
        current_user (UserOut): Usuario autenticado.

    Returns:
        dict: Contiene el access_token, tipo y tiempo de expiración en segundos.

    Raises:
        HTTPException: Si el email ya existe, la contraseña es incorrecta
                       o falla la actualización en base de datos.
    """
    # Validar actualización de email
    if user_data.email and (user_data.email != current_user.email):
        email_exists = await get_user_email(email=user_data.email)
        if email_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered."
            )

    # Validar actualización de contraseña
    if user_data.password:
        check_password = check_password_hash(current_user.password, user_data.password)
        if not check_password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Old password is incorrect!!"
            )
        user_data.new_password = generate_password_hash(user_data.new_password)

    # Preparar datos para actualización
    password_updated = user_data.password or current_user.password
    email_updated = user_data.email or current_user.email
    user_update = UserUpdate(
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        email=email_updated,
        id=current_user.id,
        password=password_updated
    )

    # Actualizar usuario en base de datos
    updated = await user_service.update_user(user_update)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating user."
        )

    # Generar nuevo token
    access_token, access_token_expires = create_access_token(email_updated)

    return {
        "access_token": access_token,
        "token_type": "Bearer",
        "expire": int(access_token_expires.total_seconds())
    }


@router.get(
    "/me",
    response_model=UserBase,
    status_code=status.HTTP_200_OK
)
async def profile(current_user: UserOut = Depends(get_current_user)):
    """
    Obtiene la información del perfil del usuario actual.

    Args:
        current_user (UserOut): Usuario autenticado.

    Returns:
        UserBase: Datos básicos del usuario.
    """
    return UserBase(
        first_name=current_user.first_name,
        last_name=current_user.last_name,
        email=current_user.email
    )
