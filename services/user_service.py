"""
Servicio de usuarios.

Provee métodos para CRUD de usuarios utilizando la base de datos
y los schemas definidos en UserOut, UserFilter, UserInsert, UserUpdate.
"""

from typing import Optional, List

from db.connnection import db_management
from schemas.user import UserOut, UserFilter, UserInsert, UserUpdate


class UserService:
    """
    Clase de servicio para operaciones relacionadas con usuarios.
    """

    @staticmethod
    async def get_users(filters: UserFilter) -> List[UserOut]:
        """
        Retorna una lista de usuarios filtrados según los criterios proporcionados.

        Args:
            filters (UserFilter): Filtros para la consulta.

        Returns:
            List[UserOut]: Lista de usuarios.
        """
        query = (
            "SELECT * FROM get_users($1::TEXT, $2::TEXT, $3::TEXT, $4::INTEGER);"
        )
        params = list(filters.model_dump().values())
        async with db_management.get_connection() as conn:
            rows = await conn.fetch(query, *params)
            return [UserOut(**dict(row)) for row in rows]

    @staticmethod
    async def insert_user(user_insert: UserInsert) -> Optional[int]:
        """
        Inserta un nuevo usuario en la base de datos.

        Args:
            user_insert (UserInsert): Datos del usuario a insertar.

        Returns:
            Optional[int]: ID del nuevo usuario si se creó correctamente.
        """
        query = (
            "SELECT * FROM insert_user($1::TEXT, $2::TEXT, $3::TEXT, $4::TEXT);"
        )
        params = list(user_insert.model_dump().values())
        async with db_management.get_connection() as conn:
            new_id = await conn.fetchval(query, *params)
            return new_id

    @staticmethod
    async def update_user(user_update: UserUpdate) -> bool:
        """
        Actualiza un usuario existente.

        Args:
            user_update (UserUpdate): Datos del usuario a actualizar.

        Returns:
            bool: True si se actualizó correctamente, False si no.
        """
        query = (
            "SELECT update_user($1::TEXT, $2::TEXT, $3::TEXT, $4::INTEGER, $5::TEXT);"
        )
        params = list(user_update.model_dump().values())
        async with db_management.get_connection() as conn:
            updated = await conn.fetchval(query, *params)
            return bool(updated)


# Instancia del servicio para uso en otros módulos
user_service = UserService()
