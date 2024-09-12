from abc import ABC

#No puede instanciarse
class Abstract_security(ABC):
        
    @abstractmethod
    def encrypt_password(password:str) -> str:
        pass
    
    @abstractmethod
    def password_check(password_encrypted:str, plain_password:str) -> bool:
        pass