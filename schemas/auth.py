from pydantic import BaseModel, EmailStr, model_validator
from typing import Optional

# Esquema de respuesta
class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    expire: int

#Para manejar entrada de datos para login
class LoginAuth(BaseModel):
    email : EmailStr
    password : str

#Para manejar creacion de cuentas
class RegisterAuth(LoginAuth):
    first_name : Optional[str] = None
    last_name : Optional[str] = None
    confirm_password : str
    
    #Validacion de que la password y confirmacion coincidan
    @model_validator(mode='after')
    def check_password_match(self):
        if self.password != self.confirm_password:
            raise ValueError('Passwords do not match')
        return self