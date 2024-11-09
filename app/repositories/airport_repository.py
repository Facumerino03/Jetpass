from sqlalchemy.exc import IntegrityError
import logging
from typing import List
from app.models import Airport
from app import db
from app.repositories.base_repository import CreateAbstractRepository, ReadAbstractRepository, UpdateAbstractRepository, DeleteAbstractRepository

class AirportRepository(CreateAbstractRepository, ReadAbstractRepository, UpdateAbstractRepository, DeleteAbstractRepository):
    
    def save(self, airport: Airport) -> Airport:
        try:
            db.session.add(airport)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            logging.error(f'error saving airport: {e}')
            raise ValueError("An airport with the same code already exists.")
        return airport
      
    def find_all(self) -> List[Airport]:
        return Airport.query.all()

    def find_by(self, **kargs) -> List[Airport]:
        return Airport.query.filter_by(**kargs).all()
        
    def find(self, id: int) -> Airport:
        result = None
        if id is not None:
            try:
                result = Airport.query.get(id)
            except Exception as e:
                logging.error(f'error getting airport by id: {id}, {e}')
        return result
    
    def delete(self, airport: Airport) -> None:
        existing_airport = self.find(airport.id)
        if existing_airport:
            db.session.delete(existing_airport)
            db.session.commit()
        else:
            logging.error(f'error deleting airport by id: {airport.id}')
    
    def update(self, airport: Airport, id: int) -> Airport:
        existing_airport = self.find(id)
        
        if existing_airport is None:
            return None
        
        existing_airport.name = airport.name
        existing_airport.airport_code = airport.airport_code
        existing_airport.city = airport.city
        existing_airport.country = airport.country
        existing_airport.south_coordinates = airport.south_coordinates
        existing_airport.west_coordinates = airport.west_coordinates
        existing_airport.latitude = airport.latitude
        existing_airport.elevation = airport.elevation
        existing_airport.runway_length = airport.runway_length
        existing_airport.traffic_type_allowed = airport.traffic_type_allowed
        
        try:
            db.session.add(existing_airport)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            logging.error(f'error updating airport: {e}')
            raise ValueError("An airport with the same code already exists.")
        return existing_airport