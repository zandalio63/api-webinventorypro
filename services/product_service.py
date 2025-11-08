"""
Servicio de productos.

Provee métodos para CRUD y búsquedas de productos utilizando la base de datos
y los schemas definidos en ProductOut, ProductFilter, ProductUpdate, ProductDelete, ProductInsert.
"""

from typing import Optional, List

from db.connnection import db_management
from schemas.product import ProductOut, ProductFilter, ProductUpdate, ProductDelete, ProductInsert


class ProductService:
    """
    Clase de servicio para operaciones relacionadas con productos.
    """

    @staticmethod
    async def get_products(filters: ProductFilter) -> List[ProductOut]:
        """
        Retorna una lista de productos filtrados según los criterios proporcionados.

        Args:
            filters (ProductFilter): Filtros para la consulta.

        Returns:
            List[ProductOut]: Lista de productos.
        """
        query = (
            "SELECT * FROM get_products($1::TEXT, $2::INTEGER, $3::NUMERIC, "
            "$4::INTEGER, $5::TIMESTAMPTZ, $6::TIMESTAMPTZ, $7::INTEGER);"
        )
        params = list(filters.model_dump().values())
        async with db_management.get_connection() as conn:
            rows = await conn.fetch(query, *params)
            return [ProductOut(**dict(row)) for row in rows]

    @staticmethod
    async def get_search_products(filters: ProductFilter) -> List[ProductOut]:
        """
        Retorna productos utilizando una búsqueda más flexible según los filtros.

        Args:
            filters (ProductFilter): Filtros de búsqueda.

        Returns:
            List[ProductOut]: Lista de productos que coinciden con los filtros.
        """
        query = (
            "SELECT * FROM get_search_products($1::TEXT, $2::INTEGER, $3::NUMERIC, "
            "$4::INTEGER, $5::TIMESTAMPTZ, $6::TIMESTAMPTZ, $7::INTEGER);"
        )
        params = list(filters.model_dump().values())
        async with db_management.get_connection() as conn:
            rows = await conn.fetch(query, *params)
            return [ProductOut(**dict(row)) for row in rows]

    @staticmethod
    async def insert_product(product_insert: ProductInsert) -> Optional[int]:
        """
        Inserta un nuevo producto en la base de datos.

        Args:
            product_insert (ProductInsert): Datos del producto a insertar.

        Returns:
            Optional[int]: ID del nuevo producto si se creó correctamente.
        """
        query = "SELECT * FROM insert_products($1, $2, $3, $4);"
        params = list(product_insert.model_dump().values())
        async with db_management.get_connection() as conn:
            new_id = await conn.fetchval(query, *params)
            return new_id

    @staticmethod
    async def update_product(product_update: ProductUpdate) -> bool:
        """
        Actualiza un producto existente.

        Args:
            product_update (ProductUpdate): Datos del producto a actualizar.

        Returns:
            bool: True si se actualizó correctamente, False si no.
        """
        query = (
            "SELECT * FROM update_products($1::TEXT, $2::INTEGER,"
            "$3::NUMERIC, $4::INTEGER, $5::INTEGER);"
        )
        params = list(product_update.model_dump().values())
        async with db_management.get_connection() as conn:
            updated = await conn.fetchval(query, *params)
            return bool(updated)

    @staticmethod
    async def delete_product(product_delete: ProductDelete) -> bool:
        """
        Elimina un producto según su ID y el ID del usuario propietario.

        Args:
            product_delete (ProductDelete): Datos del producto a eliminar.

        Returns:
            bool: True si se eliminó correctamente, False si no.
        """
        query = "SELECT * FROM delete_products($1::INTEGER, $2::INTEGER);"
        params = list(product_delete.model_dump().values())
        async with db_management.get_connection() as conn:
            deleted = await conn.fetchval(query, *params)
            return bool(deleted)


# Instancia del servicio para uso en otros módulos
product_service = ProductService()
