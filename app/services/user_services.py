from app.repositories import UserRepository
from app.models import User
from typing import List
from app.services.security import WerkzeugSecurity
from app.services.security_manager import Security

class UserServices:
    """Clase que se encarga del CRUD de los usuarios"""
    
    def __init__(self):
        self.user_repository = UserRepository()
    
    def save(self, user: User) -> User:
        if user.id is None:
            security = Security(WerkzeugSecurity())
            user.password = security.encrypt_password(user.password)
        user = self.user_repository.save(user)
        return user
    
    def update(self, user: User, id: int) -> User:
        if user.password is not None:
            security = Security(WerkzeugSecurity())
            user.password = security.encrypt_password(user.password)
        
        return self.user_repository.update(user, id)
    
    def find_all(self) -> List['User']:
        users = self.user_repository.find_all()
        return users

    def find_by(self, **kargs) -> List['User']:
        users = self.user_repository.find_by(**kargs)
        return users
        
    def find(self, id:int) -> 'User':
        user = self.user_repository.find(id)
        return user
    
    def delete(self, id:int) -> None:
        user = self.user_repository.find(id)
        if user:
            self.user_repository.delete(user)
