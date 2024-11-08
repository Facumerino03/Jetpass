import logging
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
    def update(user: User, id: int) -> User:
        entity = UserRepository.find(id)
        
        if entity is None:
            return None
        
        entity.firstname = user.firstname
        entity.lastname = user.lastname
        entity.dni = user.dni
        entity.email = user.email
        entity.phone = user.phone
        entity.address = user.address
        entity.state = user.state
        entity.city = user.city
        entity.zipcode = user.zipcode
        
        if user.password is not None:
            entity.password = user.password
        
        db.session.add(entity)
        db.session.commit()
        return entity
        
    
    @staticmethod   
    def find_all() -> List[User]:
        return User.query.all()

    @staticmethod
    def find_by(**kargs) -> List[User]:
        return User.query.filter_by(**kargs).all()
        
    @staticmethod
    def find(id: int) -> User:
        result = None
        if id is not None:
            try:
                result = User.query.get(id)
            except Exception as e:
                logging.error(f'error getting user by id: {id}, {e}') 
        return result
    
    @staticmethod
    def delete(id: int) -> None:
        user = UserRepository.find(id)
        if user:
            db.session.delete(user)
            db.session.commit()
        else:
            logging.error(f'error deleting user by id: {id}')