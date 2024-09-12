from werkzeug.security import generate_password_hash, check_password_hash
from passlib.hash import pbkdf2_sha256
from .security import AbstractSecurity

class Security:
    
    def __init__(self, security: AbstractSecurity) -> None:
        self.__security = security
    
    def encrypt_password(self, password:str) -> str:
        password_encrypted = self.__security.encrypt_password(password)
        return password_encrypted
    
    def check_password(self, password_encrypted:str, plain_password:str) -> bool:
        return self.__security.check_password(password_encrypted, plain_password)