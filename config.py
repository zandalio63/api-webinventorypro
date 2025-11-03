from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    secret_key_jwt : str
    access_token_expire_minutes : int
    access_token_expires_minutes_refresh : int
    database_url : str
    
    allowed_origins : str
    allowed_credentials : str
    allowed_methods : str
    allowed_headers : str
    
    class Config:
        env_file = ".env"
        
settings = Settings()