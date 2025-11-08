"""
Schemas de productos para la API.

Define modelos Pydantic para filtrado, inserción, actualización,
eliminación y salida de productos.
"""

from datetime import datetime
from typing import Optional
from decimal import Decimal
from pydantic import BaseModel, Field

class ProductFilterBase(BaseModel):
    """
    Modelo base para filtrar productos.

    Atributos opcionales para buscar productos por:
        name, stock, price, id, created_at, updated_at
    """
    name: Optional[str] = Field(None, description="Filter by product name")
    stock: Optional[int] = Field(None, description="Filter by stock quantity")
    price: Optional[Decimal] = Field(None, description="Filter by product price")
    id: Optional[int] = Field(None, description="Filter by product ID")
    created_at: Optional[datetime] = Field(
        None, description="Filter by creation date (from)"
    )
    updated_at: Optional[datetime] = Field(
        None, description="Filter by last update date (from)"
    )


class ProductFilter(ProductFilterBase):
    """
    Modelo de filtrado extendido que incluye el ID del usuario.
    """
    user_id: Optional[int] = Field(None, description="Filter by user ID (owner)")


class BaseProduct(BaseModel):
    """
    Modelo base de un producto.

    Atributos:
        name (str): Nombre del producto.
        stock (int): Cantidad en inventario (>= 0).
        price (Decimal): Precio del producto (>= 0.00).
    """
    name: str = Field(..., description="Product name")
    stock: int = Field(0, ge=0, description="Number of items in stock (must be non-negative)")
    price: Decimal = Field(
        Decimal("0.00"),
        ge=Decimal("0.00"),
        description="Product price (must be zero or positive)"
    )


class ProductInsert(BaseProduct):
    """
    Modelo para la inserción de un nuevo producto.

    Incluye el ID del usuario que lo posee.
    """
    user_id: int = Field(..., description="ID of the user who owns the product")


class ProductUpdate(ProductInsert):
    """
    Modelo para la actualización de un producto existente.

    Incluye el ID único del producto.
    """
    id: int = Field(..., description="Unique product identifier")


class ProductDelete(BaseModel):
    """
    Modelo para la eliminación de un producto.

    Necesita el ID del producto y el ID del usuario propietario.
    """
    id: int = Field(..., description="Product ID to delete")
    user_id: int = Field(..., description="ID of the user who owns the product")


class ProductOut(ProductUpdate):
    """
    Modelo de salida de un producto.

    Incluye información de creación y actualización de timestamps.
    """
    created_at: datetime = Field(..., description="Timestamp when the product was created")
    updated_at: Optional[datetime] = Field(
        None,
        description="Timestamp when the product was last updated"
    )
