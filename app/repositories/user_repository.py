from sqlalchemy.exc import IntegrityError # type: ignore
import logging
from typing import List
from app.models import User
from app import db
from app.repositories.base_repository import CreateAbstractRepository, ReadAbstractRepository, DeleteAbstractRepository

class UserRepository(CreateAbstractRepository, ReadAbstractRepository, DeleteAbstractRepository):
    '''
    Class representing the users repository (interacts with the database)
    '''
    def save(self, user: User) -> User:
        '''
        Saves a user to the database
        param:
            user: User
        return:
            User: The saved user
        '''
        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            logging.error(f'error saving user: {e}')
            raise ValueError("A user with the same DNI or email already exists.")
        return user
    
    def update(self, user: User, id: int) -> User:
        '''
        Updates a user in the database
        param:
            user: User
            id: int
        return:
            User: The updated user
        '''
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
        '''
        Finds all users
        return:
            List[User]: The list of users found
        '''
        return User.query.all()
    
    def find_by(self, **kargs) -> List[User]:
        '''
        Finds users by a given criteria
        param:
            kargs: dict
        return:
            List[User]: The list of users found
        '''
        return User.query.filter_by(**kargs).all()
    
    def find(self, id: int) -> User:
        '''
        Finds a user by its id
        param:
            id: int
        return:
            User: The user found
        '''
        result = None
        if id is not None:
            try:
                result = User.query.get(id)
            except Exception as e:
                logging.error(f'error getting user by id: {id}, {e}') 
        return result
    
    def delete(self, user: User) -> None:
        '''
        Deletes a user from the database
        param:
            user: User
        '''
        existing_user = self.find(user.id)
        if existing_user:
            db.session.delete(existing_user)
            db.session.commit()
        else:
            logging.error(f'error deleting user by id: {user.id}')