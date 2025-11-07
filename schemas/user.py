from pydantic import BaseModel, EmailStr, model_validator
from datetime import datetime
from typing import Optional

# Base común con todos los campos posibles
class UserBase(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None

# Para insertar un usuario nuevo
class UserInsert(UserBase):
    password: str  # requerido solo al crear

# Para actualizar un usuario existente
class UserUpdate(UserBase):
    id: int
    password: Optional[str] = None  # opcional (no siempre se actualiza)

# Para filtrar (por ID o cualquier otro campo)
class UserFilter(UserBase):
    id: Optional[int] = None

# Para respuesta de lectura
class UserOut(UserBase):
    id: int
    password: Optional[str] = None  # normalmente no se retorna
    created_at: datetime
    updated_at: Optional[datetime]

# Para actualizar perfil
class ProfileUpdate(UserBase):
    password : Optional[str] = None
    new_password : Optional[str] = None
    new_confirm_password : Optional[str] = None
    
    @model_validator(mode='after')
    def check_password_match(self):
        # Si se quiere cambiar la contraseña
        if self.new_password or self.new_confirm_password:
            if not self.password:
                raise ValueError("Current password is required to update the password")
            
            if not self.new_password or not self.new_confirm_password:
                raise ValueError("Both new_password and new_confirm_password must be provided")
            
            if self.new_password != self.new_confirm_password:
                raise ValueError("New passwords do not match")
        
        # Si no se está cambiando la contraseña, no hacer nada
        return self