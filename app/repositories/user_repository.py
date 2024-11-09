from sqlalchemy.exc import IntegrityError
import logging
from typing import List
from app.models import User
from app import db
from app.repositories.base_repository import CreateAbstractRepository, ReadAbstractRepository, DeleteAbstractRepository

class UserRepository(CreateAbstractRepository, ReadAbstractRepository, DeleteAbstractRepository):
    
    def save(self, user: User) -> User:
        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            logging.error(f'error saving user: {e}')
            raise ValueError("A user with the same DNI or email already exists.")
        return user
    
    def update(self, user: User, id: int) -> User:
        entity = self.find(id)
        
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
        
        try:
            db.session.add(entity)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            logging.error(f'error updating user: {e}')
            raise ValueError("A user with the same DNI or email already exists.")
        return entity
    
    def find_all(self) -> List[User]:
        return User.query.all()
    
    def find_by(self, **kargs) -> List[User]:
        return User.query.filter_by(**kargs).all()
    
    def find(self, id: int) -> User:
        result = None
        if id is not None:
            try:
                result = User.query.get(id)
            except Exception as e:
                logging.error(f'error getting user by id: {id}, {e}') 
        return result
    
    def delete(self, user: User) -> None:
        existing_user = self.find(user.id)
        if existing_user:
            db.session.delete(existing_user)
            db.session.commit()
        else:
            logging.error(f'error deleting user by id: {user.id}')