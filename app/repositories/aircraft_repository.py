import logging
from typing import List
from app.models import Aircraft
from app import db
from app.repositories.base_repository import CreateAbstractRepository, ReadAbstractRepository, UpdateAbstractRepository, DeleteAbstractRepository

class AircraftRepository(CreateAbstractRepository, ReadAbstractRepository, UpdateAbstractRepository, DeleteAbstractRepository):
    
    def save(self, aircraft: Aircraft) -> Aircraft:
        db.session.add(aircraft)
        db.session.commit()
        return aircraft
      
    def find_all(self) -> List[Aircraft]:
        return Aircraft.query.all()

    def find_by(self, **kargs) -> List[Aircraft]:
        return Aircraft.query.filter_by(**kargs).all()
        
    def find(self, id: int) -> Aircraft:
        result = None
        if id is not None:
            try:
                result = Aircraft.query.get(id)
            except Exception as e:
                logging.error(f'error getting pilot by id: {id}, {e}') 
        return result
    
    def delete(self, aircraft: Aircraft) -> None:
        existing_aircraft = self.find(aircraft.id)
        if existing_aircraft:
            db.session.delete(existing_aircraft)
            db.session.commit()
        else:
            logging.error(f'error deleting user by id: {aircraft.id}')
    
    def update(self, aircraft: Aircraft) -> Aircraft:
        existing_aircraft = self.find(aircraft.id)
        
        if existing_aircraft is None:
            return None
        
        existing_aircraft.aircraft_identification = aircraft.aircraft_identification
        existing_aircraft.aircraft_type = aircraft.aircraft_type
        existing_aircraft.wake_turbulence_category = aircraft.wake_turbulence_category
        existing_aircraft.equipment = aircraft.equipment
        existing_aircraft.endurance = aircraft.endurance
        existing_aircraft.passenger_capacity = aircraft.passenger_capacity
        existing_aircraft.crew_capacity = aircraft.crew_capacity
        existing_aircraft.max_speed = aircraft.max_speed
        existing_aircraft.aircraft_colour_and_marking = aircraft.aircraft_colour_and_marking
        
        db.session.commit()
        return existing_aircraft