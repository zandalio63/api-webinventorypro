from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bycript"], deprecated="auto")

def hash_password(password : str) -> str :
    """
    Se encarga de hashear la password
    """
    return pwd_context.hash(password)

def verify_password(plain_password : str, hashed : str) -> bool :
    """
    Se encarga de verificar la contraseña
    """
    return pwd_context.verify(plain_password, hashed)