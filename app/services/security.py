from werkzeug.security import generate_password_hash, check_password_hash
from passlib.hash import pbkdf2_sha256 # type: ignore
from abc import ABC, abstractmethod

class AbstractSecurity(ABC):
    '''
    Abstract class that handles the security
    '''
        
    @abstractmethod
    def encrypt_password(self, password:str) -> str:
        pass
    
    @abstractmethod
    def check_password(self, password_encrypted:str, plain_password:str) -> bool:
        pass
    
class WerkzeugSecurity(AbstractSecurity):
    '''
    Class that handles the security using werkzeug
    '''
    
    def encrypt_password(self, password:str) -> str:
        password_encrypted = generate_password_hash(password)
        return password_encrypted
    
    def check_password(self, password_encrypted:str, plain_password:str) -> bool:
        return check_password_hash(password_encrypted, plain_password)
    
class PasslibSecurity(AbstractSecurity):
    '''
    Class that handles the security using passlib
    '''
    
    def encrypt_password(self, password:str) -> str:
        password_encrypted = pbkdf2_sha256.hash(password)
        return password_encrypted
    
    def check_password(self, password_encrypted:str, plain_password:str) -> bool:
        return pbkdf2_sha256.verify(plain_password, password_encrypted)
    
    