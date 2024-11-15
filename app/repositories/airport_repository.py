from sqlalchemy.exc import IntegrityError # type: ignore
import logging
from typing import List
from app.models import Airport
from app import db
from app.repositories.base_repository import CreateAbstractRepository, ReadAbstractRepository, UpdateAbstractRepository, DeleteAbstractRepository

class AirportRepository(CreateAbstractRepository, ReadAbstractRepository, UpdateAbstractRepository, DeleteAbstractRepository):
    '''
    Class representing the airports repository (interacts with the database)
    '''
    def save(self, airport: Airport) -> Airport:
        '''
        Saves an airport to the database
        param:
            airport: Airport
        return:
            Airport: The saved airport
        '''
        try:
            db.session.add(airport)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            logging.error(f'error saving airport: {e}')
            raise ValueError("An airport with the same code already exists.")
        return airport
      
    def find_all(self) -> List[Airport]:
        '''
        Finds all airports
        return:
            List[Airport]: The list of airports found
        '''
        return Airport.query.all()

    def find_by(self, **kargs) -> List[Airport]:
        '''
        Finds airports by a given criteria
        param:
            kargs: dict
        return:
            List[Airport]: The list of airports found
        '''
        return Airport.query.filter_by(**kargs).all()
        
    def find(self, id: int) -> Airport:
        '''
        Finds an airport by its id
        param:
            id: int
        return:
            Airport: The airport found
        '''
        result = None
        if id is not None:
            try:
                result = Airport.query.get(id)
            except Exception as e:
                logging.error(f'error getting airport by id: {id}, {e}')
        return result
    
    def delete(self, airport: Airport) -> None:
        '''
        Deletes an airport from the database
        param:
            airport: Airport
        '''
        existing_airport = self.find(airport.id)
        if existing_airport:
            db.session.delete(existing_airport)
            db.session.commit()
        else:
            logging.error(f'error deleting airport by id: {airport.id}')
    
    def update(self, airport: Airport, id: int) -> Airport:
        '''
        Updates an airport in the database
        param:
            airport: Airport
            id: int
        return:
            Airport: The updated airport
        '''
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