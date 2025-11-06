from typing import Optional, List

from db.connnection import db_management
from schemas.product import ProductOut, ProductFilter, BaseProduct, ProductUpdate, ProductDelete

class ProductService:
    @staticmethod
    async def get_products(filters : ProductFilter) -> List[ProductFilter]:
        query = "SELECT * FROM get_products($1::TEXT, $2::INTEGER, $3::NUMERIC, $4::INTEGER, $5::INTEGER, $6::TIMESTAMPTZ, $7::TIMESTAMPTZ);"
        params = list(filters.model_dump().values())
        async with db_management.get_connection() as conn:
            rows = await conn.fetch(query, *params)
            return [ProductOut(**dict(row)) for row in rows]
        
    @staticmethod
    async def insert_product(product_insert : BaseProduct) -> Optional[int]:
        query = "SELECT * FROM insert_products($1, $2, $3, $4);"
        params = list(product_insert.model_dump().values())
        async with db_management.get_connection() as conn:
            new_id = await conn.fetchval(query, *params)
            return new_id
    
    @staticmethod
    async def update_product(product_update : ProductUpdate) -> bool:
        query = "SELECT * FROM update_products($1::TEXT, $2::INTEGER, $3::NUMERIC, $4::INTEGER, $5::INTEGER);"
        params = list(product_update.model_dump().values())
        async with db_management.get_connection() as conn:
            updated = await conn.fetchval(query, params)
            return bool(updated)
    
    @staticmethod
    async def delete_product(product_delete : ProductDelete) -> bool:
        query = "SELECT * FROM delete_products($1::INTEGER, $2::INTEGER);"
        params = list(product_delete.model_dump().values())
        async with db_management.get_connection() as conn:
            deleted = await conn.fetchval(query, params)
            return bool(deleted)

product_service = ProductService()