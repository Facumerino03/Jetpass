from typing import List
from app.models import Airport
from app.repositories import AirportRepository

class AirportServices:
    '''
    Class that handles the CRUD of the airports
    '''
    def __init__(self):
        self.airport_repository = AirportRepository()

    def save(self, airport: Airport) -> Airport:
        '''
        Saves an airport
        
        param:
            airport: Airport
        return:
            Airport
        '''
        return self.airport_repository.save(airport)

    def update(self, airport: Airport, id: int) -> Airport:
        '''
        Updates an airport
        
        param:
            airport: Airport
            id: int
        return:
            Airport
        '''
        return self.airport_repository.update(airport, id)

    def find_all(self) -> List[Airport]:
        '''
        Finds all airports
        
        return:
            List[Airport]
        '''
        airports = self.airport_repository.find_all()
        return airports

    def find_by(self, **kargs) -> List[Airport]:
        '''
        Finds airports by the given arguments
        
        param:
            **kargs: dict
        return:
            List[Airport]
        '''
        airports = self.airport_repository.find_by(**kargs)
        return airports

    def find(self, id: int) -> Airport:
        '''
        Finds an airport by its id
        
        param:
            id: int
        return:
            Airport
        '''
        airport = self.airport_repository.find(id)
        return airport

    def delete(self, id: int) -> None:
        '''
        Deletes an airport by its id
        
        param:
            id: int
        '''
        airport = self.airport_repository.find(id)
        if airport:
            self.airport_repository.delete(airport)