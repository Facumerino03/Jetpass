from werkzeug.security import generate_password_hash, check_password_hash
from passlib.hash import pbkdf2_sha256

class Security:
    
    @staticmethod
    def encrypt_password(password:str) -> str:
        password_encrypted = generate_password_hash(password)
        return password_encrypted
    
    @staticmethod
    def password_check(password_encrypted:str, plain_password:str) -> bool:
        return check_password_hash(password_encrypted, plain_password)
    
    @staticmethod
    def encrypt_password_passlib(password:str) -> str:
        password_encrypted = pbkdf2_sha256.hash(password)
        return password_encrypted
    
    @staticmethod
    def password_check_passlib(password_encrypted:str, plain_password:str) -> bool:
        return pbkdf2_sha256.verify(plain_password, password_encrypted)

    @staticmethod
    def encrypt_password_xyz(password:str) -> str:
        password_encrypted = pbkdf2_sha256.hash(password)
        return password_encrypted
    
    @staticmethod
    def password_check_xyz(password_encrypted:str, plain_password:str) -> bool:
        return pbkdf2_sha256.verify(plain_password, password_encrypted)