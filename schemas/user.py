from pydantic import BaseModel, EmailStr
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