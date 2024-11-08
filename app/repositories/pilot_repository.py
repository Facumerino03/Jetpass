import logging
import re
from typing import List
from app.models import Pilot
from app import db
from app.repositories.base_repository import CreateAbstractRepository, ReadAbstractRepository, UpdateAbstractRepository, DeleteAbstractRepository

class PilotRepository(CreateAbstractRepository, ReadAbstractRepository, UpdateAbstractRepository, DeleteAbstractRepository):
    
    def save(self, pilot: Pilot) -> Pilot:
        db.session.add(pilot)
        db.session.commit()
        return pilot
      
    def find_all(self) -> List[Pilot]:
        return Pilot.query.all()
    
    def find_by(self, **kargs) -> List[Pilot]:
        return Pilot.query.filter_by(**kargs).all()
        
    def find(self, id: int) -> Pilot:
        result = None
        if id is not None:
            try:
                result = Pilot.query.get(id)
            except Exception as e:
                logging.error(f'error getting pilot by id: {id}, {e}') 
        return result
    
    def delete(self, pilot: Pilot) -> None:
        existing_pilot = self.find(pilot.id)
        if existing_pilot:
            db.session.delete(existing_pilot)
            db.session.commit()
        else:
            logging.error(f'error deleting user by id: {pilot.id}')
    
    def update(self, pilot: Pilot) -> Pilot:
        existing_pilot = self.find(pilot.id)
        
        if existing_pilot is None:
            return None
        
        existing_pilot.first_name = pilot.first_name
        existing_pilot.last_name = pilot.last_name
        existing_pilot.license_number = pilot.license_number
        db.session.commit()
        return existing_pilot
    