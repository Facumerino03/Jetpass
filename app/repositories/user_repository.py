from typing import List
from app.models import User
from app import db
from app.repositories.base_repository import CreateAbstractRepository, ReadAbstractRepository, DeleteAbstractRepository

class UserRepository(CreateAbstractRepository, ReadAbstractRepository, DeleteAbstractRepository):
    
    @staticmethod
    def save(user: User) -> User:
        db.session.add(user)
        db.session.commit()
        return user
   
    @staticmethod   
    def find_all() -> List[User]:
        return User.query.all()

    @staticmethod
    def find_by(**kargs) -> List[User]:
        return User.query.filter_by(**kargs).all()
        
    @staticmethod
    def find(id: int) -> User:
        return User.query.get(id)
    
    @staticmethod
    def delete(user: User) -> None:
        db.session.delete(user)
        db.session.commit()