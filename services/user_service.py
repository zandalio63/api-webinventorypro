from typing import Optional, List

from db.connnection import db_management
from schemas.user import UserOut, UserFilter, UserInsert, UserUpdate


class UserService:
    @staticmethod
    async def get_users(filters : UserFilter) -> List[UserOut]:
        query = "SELECT * FROM get_users($1::TEXT, $2::TEXT, $3::TEXT, $4::INTEGER);"
        params = list(filters.model_dump().values())
        async with db_management.get_connection() as conn:
            rows = await conn.fetch(query, *params)
            return [UserOut(**dict(row)) for row in rows]
        
    @staticmethod
    async def insert_user(user_insert : UserInsert) -> Optional[int]:
        query = "SELECT * FROM insert_user($1::TEXT, $2::TEXT, $3::TEXT, $4::TEXT);"
        params = list(user_insert.model_dump().values())
        async with db_management.get_connection() as conn:
            new_id = await conn.fetchval(query, *params)
            return new_id
    
    @staticmethod
    async def update_user(user_update: UserUpdate) -> bool:
        query = "SELECT update_user($1, $2, $3, $4, $5);"
        params = list(user_update.model_dump().values())
        async with db_management.get_connection() as conn:
            updated = await conn.fetchval(query, *params)
            return bool(updated)

user_service = UserService()