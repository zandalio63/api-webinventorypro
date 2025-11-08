"""
Módulo de rutas para la gestión de productos.

Este módulo define los endpoints de la API relacionados con productos, incluyendo:
- Listado de productos del usuario.
- Consulta de un producto por ID.
- Búsqueda de productos con filtros.
- Creación de nuevos productos.
- Actualización de productos existentes.
- Eliminación de productos.

Cada endpoint requiere autenticación mediante `get_current_user`.
"""

from typing import List
from fastapi import APIRouter, HTTPException, status, Depends

from schemas.product import (
    ProductOut, ProductFilter, BaseProduct, ProductInsert,
    ProductFilterBase, ProductDelete, ProductUpdate
)
from schemas.user import UserOut
from core.dependencies import get_current_user
from services.product_service import product_service

router = APIRouter(prefix='/products', tags=["Products"])


@router.get("/", response_model=List[ProductOut], status_code=status.HTTP_200_OK)
async def get_products(current_user: UserOut = Depends(get_current_user)):
    """
    Retorna todos los productos del usuario actual.

    Args:
        current_user (UserOut): Usuario autenticado.

    Returns:
        List[ProductOut]: Lista de productos del usuario.
    """
    return await product_service.get_products(ProductFilter(user_id=current_user.id))


@router.get("/{product_id}", response_model=ProductOut, status_code=status.HTTP_200_OK)
async def get_product_by_id(
    product_id: int,
    current_user: UserOut = Depends(get_current_user)
):
    """
    Retorna un producto por su ID del usuario actual.

    Args:
        product_id (int): ID del producto a consultar.
        current_user (UserOut): Usuario autenticado.

    Returns:
        ProductOut: Producto correspondiente al ID.

    Raises:
        HTTPException: Si el producto no se encuentra (404).
    """
    products = await product_service.get_products(
        ProductFilter(id=product_id, user_id=current_user.id)
    )
    if not products:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    return products[0]


@router.post("/filter", response_model=List[ProductOut], status_code=status.HTTP_200_OK)
async def get_search_products(
    product_filters: ProductFilterBase,
    current_user: UserOut = Depends(get_current_user)
):
    """
    Retorna productos filtrados según los criterios enviados.

    Args:
        product_filters (ProductFilterBase): Filtros de búsqueda.
        current_user (UserOut): Usuario autenticado.

    Returns:
        List[ProductOut]: Lista de productos que cumplen los filtros.
    """
    return await product_service.get_search_products(
        ProductFilter(**product_filters.model_dump(), user_id=current_user.id)
    )


@router.post("/", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
async def create_product(
    product_data: BaseProduct,
    current_user: UserOut = Depends(get_current_user)
):
    """
    Crea un nuevo producto para el usuario actual.

    Args:
        product_data (BaseProduct): Datos del producto a crear.
        current_user (UserOut): Usuario autenticado.

    Returns:
        ProductOut: Producto recién creado.

    Raises:
        HTTPException: Si el producto ya existe (409) o falla el registro (500).
        HTTPException: Si el producto creado no se encuentra (404).
    """
    product_exists = await product_service.get_products(
        ProductFilter(user_id=current_user.id, name=product_data.name)
    )
    if product_exists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Product already exists!!'
        )

    product_add = ProductInsert(
        name=product_data.name,
        stock=product_data.stock,
        price=product_data.price,
        user_id=current_user.id
    )

    new_id = await product_service.insert_product(product_add)
    if not new_id:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error registering product."
        )

    products = await product_service.get_products(ProductFilter(id=new_id))
    if not products:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    return products[0]


@router.put("/{product_id}", status_code=status.HTTP_200_OK)
async def update_product(
    product_id: int,
    product_data: BaseProduct,
    current_user: UserOut = Depends(get_current_user)
):
    """
    Actualiza un producto existente del usuario actual.

    Args:
        product_id (int): ID del producto a actualizar.
        product_data (BaseProduct): Nuevos datos del producto.
        current_user (UserOut): Usuario autenticado.

    Returns:
        dict: Mensaje de éxito de la actualización.

    Raises:
        HTTPException: Si el producto no existe (404).
        HTTPException: Si el nombre del producto ya está registrado (400).
        HTTPException: Si falla la actualización en base de datos (500).
    """
    products = await product_service.get_products(
        ProductFilter(user_id=current_user.id, id=product_id)
    )
    if not products:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    if product_data.name != products[0].name:
        products = await product_service.get_products(
            ProductFilter(user_id=current_user.id, name=product_data.name)
        )
        product = products[0] if products else None
        if product:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Product name already registered."
            )

    product_update = ProductUpdate(
        **product_data.model_dump(),
        id=product_id,
        user_id=current_user.id
    )

    updated = await product_service.update_product(product_update)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating product."
        )

    return {
        "message": "Product Update"
    }


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: int, current_user: UserOut = Depends(get_current_user)):
    """
    Elimina un producto del usuario actual.

    Args:
        product_id (int): ID del producto a eliminar.
        current_user (UserOut): Usuario autenticado.

    Returns:
        int: Código de estado HTTP 204 si se elimina correctamente.

    Raises:
        HTTPException: Si el producto no existe (404).
        HTTPException: Si falla la eliminación (500).
    """
    products = await product_service.get_products(
        ProductFilter(id=product_id, user_id=current_user.id)
    )

    if products:
        deleted = await product_service.delete_product(
            ProductDelete(id=products[0].id, user_id=current_user.id)
        )

        if deleted:
            return status.HTTP_204_NO_CONTENT

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deleting product."
        )

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Product not found"
    )
