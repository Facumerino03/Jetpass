from sqlalchemy.exc import IntegrityError # type: ignore
import logging
from typing import List
from app.models import Pilot
from app import db
from app.repositories.base_repository import CreateAbstractRepository, ReadAbstractRepository, UpdateAbstractRepository, DeleteAbstractRepository

class PilotRepository(CreateAbstractRepository, ReadAbstractRepository, UpdateAbstractRepository, DeleteAbstractRepository):
    '''
    Class representing the pilots repository (interacts with the database)
    '''
    def save(self, pilot: Pilot) -> Pilot:
        '''
        Saves a pilot to the database
        param:
            pilot: Pilot
        return:
            Pilot: The saved pilot
        '''
        try:
            db.session.add(pilot)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            logging.error(f'error saving pilot: {e}')
            raise ValueError("A pilot with the same license number already exists.")
        return pilot
      
    def find_all(self) -> List[Pilot]:
        '''
        Finds all pilots
        return:
            List[Pilot]: The list of pilots found
        '''
        return Pilot.query.all()
    
    def find_by(self, **kargs) -> List[Pilot]:
        '''
        Finds pilots by a given criteria
        param:
            kargs: dict
        return:
            List[Pilot]: The list of pilots found
        '''
        return Pilot.query.filter_by(**kargs).all()
        
    def find(self, id: int) -> Pilot:
        '''
        Finds a pilot by its id
        param:
            id: int
        return:
            Pilot: The pilot found
        '''
        result = None
        if id is not None:
            try:
                result = Pilot.query.get(id)
            except Exception as e:
                logging.error(f'error getting pilot by id: {id}, {e}') 
        return result
    
    def delete(self, pilot: Pilot) -> None:
        '''
        Deletes a pilot from the database
        param:
            pilot: Pilot
        '''
        existing_pilot = self.find(pilot.id)
        if existing_pilot:
            db.session.delete(existing_pilot)
            db.session.commit()
        else:
            logging.error(f'error deleting user by id: {pilot.id}')
    
    def update(self, pilot: Pilot, id: int) -> Pilot:
        '''
        Updates a pilot in the database
        param:
            pilot: Pilot
            id: int
        return:
            Pilot: The updated pilot
        '''
        existing_pilot = self.find(id)
        
        if existing_pilot is None:
            return None
        
        existing_pilot.first_name = pilot.first_name
        existing_pilot.last_name = pilot.last_name
        existing_pilot.license_number = pilot.license_number
        
        try:
            db.session.add(existing_pilot)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            logging.error(f'error updating pilot: {e}')
            raise ValueError("A pilot with the same license number already exists.")
        return existing_pilot
    