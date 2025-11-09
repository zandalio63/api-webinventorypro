"""
Schemas de autenticación y tokens para la API.

Define modelos Pydantic para login, registro de usuarios
y la respuesta de tokens JWT.
"""

from typing import Optional

from pydantic import BaseModel, EmailStr, Field, model_validator


class TokenResponse(BaseModel):
    """
    Modelo que representa la respuesta de un token JWT.

    Atributos:
        access_token (str): Token de acceso.
        token_type (str): Tipo de token (ej. "Bearer").
        expire (int): Tiempo de expiración en segundos o minutos.
    """

    access_token: str = Field(
        ..., description="Access Token required when response a user"
    )
    token_type: str = Field(..., description="Token Type required when response a user")
    expire: int = Field(..., description="Expire required when response a user")


class LoginAuth(BaseModel):
    """
    Modelo para el login de un usuario.

    Atributos:
        email (EmailStr): Correo electrónico del usuario.
        password (str): Contraseña del usuario.
    """

    email: EmailStr = Field(..., description="Email required when login user")
    password: str = Field(..., description="Password required when login a new user")


class RegisterAuth(LoginAuth):
    """
    Modelo para el registro de un usuario.

    Hereda de LoginAuth e incluye información adicional:
        first_name (Optional[str]): Nombre del usuario.
        last_name (Optional[str]): Apellido del usuario.
        confirm_password (str): Confirmación de la contraseña.
    """

    first_name: Optional[str] = Field(None, description="Users' Firstname")
    last_name: Optional[str] = Field(None, description="User's Lastname")
    confirm_password: str = Field(
        ..., description="Confirm Password required when creating a new user"
    )

    @model_validator(mode="after")
    def check_password_match(self) -> "RegisterAuth":
        """
        Valida que `password` y `confirm_password` sean iguales.

        Raises:
            ValueError: Si las contraseñas no coinciden.
        """
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match")
        return self
