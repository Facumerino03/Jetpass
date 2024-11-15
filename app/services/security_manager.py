from .security import AbstractSecurity

class Security:
    '''
    Class that handles the security
    '''
    def __init__(self, security: AbstractSecurity) -> None:
        self.__security = security
    
    def encrypt_password(self, password:str) -> str:
        '''
        Encrypts the password
        
        param:
            password: str
        return:
            str
        '''
        password_encrypted = self.__security.encrypt_password(password)
        return password_encrypted
    
    def check_password(self, password_encrypted:str, plain_password:str) -> bool:
        '''
        Checks the password
        
        param:
            password_encrypted: str
            plain_password: str
        return:
            bool
        '''
        return self.__security.check_password(password_encrypted, plain_password)