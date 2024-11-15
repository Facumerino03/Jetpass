from app.repositories import UserRepository
from app.models import User
from typing import List
from app.services.security import WerkzeugSecurity
from app.services.security_manager import Security

class UserServices:
    '''
    Class that handles the CRUD of the users
    '''
    
    def __init__(self):
        self.user_repository = UserRepository()
    
    def save(self, user: User) -> User:
        '''
        Saves the user
        
        param:
            user: User
        return:
            User
        '''
        if user.id is None:
            security = Security(WerkzeugSecurity())
            user.password = security.encrypt_password(user.password)
        user = self.user_repository.save(user)
        return user
    
    def update(self, user: User, id: int) -> User:
        '''
        Updates the user
        
        param:
            user: User
            id: int
        return:
            User
        '''
        if user.password is not None:
            security = Security(WerkzeugSecurity())
            user.password = security.encrypt_password(user.password)
        
        return self.user_repository.update(user, id)
    
    def find_all(self) -> List['User']:
        '''
        Finds all the users
        
        return:
            List[User]
        '''
        users = self.user_repository.find_all()
        return users

    def find_by(self, **kargs) -> List['User']:
        '''
        Finds the users by the given arguments
        
        param:
            **kargs: dict
        return:
            List[User]
        '''
        users = self.user_repository.find_by(**kargs)
        return users
        
    def find(self, id:int) -> 'User':
        '''
        Finds the user by its id
        
        param:
            id: int
        return:
            User
        '''
        user = self.user_repository.find(id)
        return user
    
    def delete(self, id:int) -> None:
        '''
        Deletes the user by its id
        
        param:
            id: int
        '''
        user = self.user_repository.find(id)
        if user:
            self.user_repository.delete(user)
