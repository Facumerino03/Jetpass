from werkzeug.security import generate_password_hash, check_password_hash

class Security:
    
    @staticmethod
    def encrypt_password(password:str) -> str:
        password_encrypted = generate_password_hash(password)
        return password_encrypted
    
    @staticmethod
    def password_check(password_encrypted, plain_password) -> bool:
        return check_password_hash(password_encrypted, plain_password)