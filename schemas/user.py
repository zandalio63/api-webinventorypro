"""
Schemas de usuarios para la API.

Define modelos Pydantic para la creación, actualización, filtrado y salida de usuarios,
así como para la actualización del perfil.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, model_validator


class UserBase(BaseModel):
    """
    Modelo base de un usuario.

    Incluye información opcional común para varios usos:
        first_name, last_name, email
    """

    first_name: Optional[str] = Field(None, description="User's first name")
    last_name: Optional[str] = Field(None, description="User's last name")
    email: Optional[EmailStr] = Field(None, description="User email address")


class UserInsert(UserBase):
    """
    Modelo para la inserción de un nuevo usuario.

    Incluye el password requerido para creación.
    """

    password: str = Field(..., description="Password required when creating a new user")


class UserUpdate(UserBase):
    """
    Modelo para la actualización de un usuario existente.

    Incluye ID obligatorio y password opcional para cambios.
    """

    id: int = Field(..., description="User ID to update")
    password: Optional[str] = Field(None, description="Optional password for update")


class UserFilter(UserBase):
    """
    Modelo para filtrar usuarios.

    Permite filtrar por ID además de los campos base.
    """

    id: Optional[int] = Field(None, description="User ID filter")


class UserOut(UserBase):
    """
    Modelo de salida de usuario.

    Incluye información de identificación y timestamps.
    """

    id: int = Field(..., description="Unique user identifier")
    password: Optional[str] = Field(
        None, description="Normally not returned for security reasons"
    )
    created_at: datetime = Field(..., description="Timestamp when the user was created")
    updated_at: Optional[datetime] = Field(
        None, description="Timestamp when the user was last updated"
    )


class ProfileUpdate(UserBase):
    """
    Modelo para la actualización del perfil de usuario.

    Permite cambiar la contraseña si se proporciona la actual.
    """

    password: Optional[str] = Field(
        None, description="Current password (required to change password)"
    )
    new_password: Optional[str] = Field(None, description="New password")
    new_confirm_password: Optional[str] = Field(
        None, description="New password confirmation"
    )

    @model_validator(mode="after")
    def check_password_match(self) -> "ProfileUpdate":
        """
        Valida que la nueva contraseña coincida y que se proporcione la actual.

        Raises:
            ValueError: Si la validación falla.
        """
        if self.new_password or self.new_confirm_password:
            if not self.password:
                raise ValueError("Current password is required to update the password")
            if not self.new_password or not self.new_confirm_password:
                raise ValueError(
                    "Both new_password and new_confirm_password must be provided"
                )
            if self.new_password != self.new_confirm_password:
                raise ValueError("New passwords do not match")
        return self
