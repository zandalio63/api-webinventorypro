"""
Módulo de configuración de la aplicación.

Define la clase `Settings`, que gestiona la carga de variables de entorno
usando Pydantic y dotenv. Permite acceder a claves secretas, URLs de base
de datos y otros parámetros de configuración de manera tipada y validada.
"""
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    """
    Clase de configuración principal de la aplicación.

    Atributos:
        secret_key_jwt (str): Clave secreta para firmar los JWT.
        access_token_expire_minutes (int): Minutos de expiración para el token de acceso.
        access_token_expire_minutes_refresh (int): Minutos de expiración para el token de refresco.
        database_url (str): URL de conexión a la base de datos PostgreSQL.
    """
    secret_key_jwt : str
    access_token_expire_minutes : int
    access_token_expire_minutes_refresh : int
    database_url : str

    #allowed_origins : str
    #allowed_credentials : str
    #allowed_methods : str
    #allowed_headers : str

    class Config:
        """
        Configuración interna de Pydantic.

        Define el archivo de entorno (.env) desde el cual se cargarán las
        variables de entorno automáticamente.
        """
        env_file = ".env"


settings = Settings()
