from pydantic import BaseModel, EmailStr, Field, model_validator
from typing import Optional

# Esquema de respuesta
class TokenResponse(BaseModel):
    access_token: str = Field(..., description="Access Token required when response a user")
    token_type: str = Field(..., description="Token Type required when response a user")
    expire: int = Field(..., description="Expire required when response a user")

#Para manejar entrada de datos para login
class LoginAuth(BaseModel):
    email : EmailStr = Field(..., description="Email required when login user")
    password : str = Field(..., description="Password required when login a new user")

#Para manejar creacion de cuentas
class RegisterAuth(LoginAuth):
    first_name : Optional[str] = Field(None, description="Users' Firstname")
    last_name : Optional[str] = Field(None, description="User's Lastname")
    confirm_password : str = Field(..., description="Confirm Password required when creating a new user")
    
    #Validacion de que la password y confirmacion coincidan
    @model_validator(mode='after')
    def check_password_match(self):
        if self.password != self.confirm_password:
            raise ValueError('Passwords do not match')
        return self