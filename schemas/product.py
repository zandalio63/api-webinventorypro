from typing import Optional
from decimal import Decimal
from pydantic import BaseModel, Field
from datetime import datetime

class ProductFilterBase(BaseModel):
    name: Optional[str] = Field(None, description="Filter by product name")
    stock: Optional[int] = Field(None, description="Filter by stock quantity")
    price: Optional[Decimal] = Field(None, description="Filter by product price")
    id: Optional[int] = Field(None, description="Filter by product ID")
    created_at: Optional[datetime] = Field(None, description="Filter by creation date (from)")
    updated_at: Optional[datetime] = Field(None, description="Filter by last update date (from)")

class ProductFilter(ProductFilterBase):
    user_id: Optional[int] = Field(None, description="Filter by user ID (owner)")

class BaseProduct(BaseModel):
    name: str = Field(..., description="Product name")
    stock: int = Field(0, ge=0, description="Number of items in stock (must be non-negative)")
    price: Decimal = Field(
        Decimal("0.00"),
        ge=Decimal("0.00"),
        description="Product price (must be zero or positive)"
    )
    
class ProductInsert(BaseProduct):
    user_id: int = Field(..., description="ID of the user who owns the product")
    
class ProductUpdate(ProductInsert):
    id: int = Field(..., description="Unique product identifier")

class ProductDelete(BaseModel):
    id: int = Field(..., description="Product ID to delete")
    user_id: int = Field(..., description="ID of the user who owns the product")

class ProductOut(ProductUpdate):
    created_at: datetime = Field(..., description="Timestamp when the product was created")
    updated_at: Optional[datetime] = Field(None, description="Timestamp when the product was last updated")
