from app.repositories import UserRepository
from app.models import User
from typing import List
from app.services.security import WerkzeugSecurity
from app.services.security_manager import Security


class UserServices:
    """Clase que se encarga del CRUD de los usuarios"""
    
    @staticmethod
    def save(user: User) -> User:
        if user.id is None:
            security = Security(WerkzeugSecurity())
            user.password = security.encrypt_password(user.password)
        user = UserRepository.save(user)
        return user
   
    @staticmethod   
    def find_all() -> List['User']:
        users = UserRepository.find_all()
        return users

    @staticmethod
    def find_by(**kargs) -> List['User']:
        users = UserRepository.find_by(**kargs)
        return users
        
    @staticmethod
    def find(id:int) -> 'User':
        user = UserRepository.find(id)
        return user
    
    @staticmethod
    def delete(user:User) -> None:
        UserRepository.delete(user)