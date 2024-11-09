from typing import List
from app.models import Airport
from app.repositories import AirportRepository

class AirportServices:
    """Clase que se encarga del CRUD de los aeropuertos"""
    def __init__(self):
        self.airport_repository = AirportRepository()

    def save(self, airport: Airport) -> Airport:
        return self.airport_repository.save(airport)

    def update(self, airport: Airport, id: int) -> Airport:
        return self.airport_repository.update(airport, id)

    def find_all(self) -> List[Airport]:
        airports = self.airport_repository.find_all()
        return airports

    def find_by(self, **kargs) -> List[Airport]:
        airports = self.airport_repository.find_by(**kargs)
        return airports

    def find(self, id: int) -> Airport:
        airport = self.airport_repository.find(id)
        return airport

    def delete(self, id: int) -> None:
        airport = self.airport_repository.find(id)
        if airport:
            self.airport_repository.delete(airport)