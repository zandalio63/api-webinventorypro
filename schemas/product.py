from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class BaseProduct(BaseModel):
    name: Optional[str] = None
    stock: Optional[int] = None
    user_id: Optional[int] = None
    id: Optional[int] = None

class ProductFilter(BaseProduct):
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class ProductInsert(BaseModel):
    name: str
    stock: int = 0
    user_id: int

class ProductOut(ProductInsert):
    created_at: datetime
    updated_at: Optional[datetime] = None
    id: int
