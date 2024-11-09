from typing import List
from app.models import Pilot
from app.repositories import PilotRepository

class PilotServices:
    """Clase que se encarga del CRUD de los pilotos"""
    def __init__(self):
        self.pilot_repository = PilotRepository()

    def save(self, pilot: Pilot) -> Pilot:
        return self.pilot_repository.save(pilot)

    def update(self, pilot: Pilot, id: int) -> Pilot:
        return self.pilot_repository.update(pilot, id)

    def find_all(self) -> List[Pilot]:
        pilots = self.pilot_repository.find_all()
        return pilots

    def find_by(self, **kargs) -> List[Pilot]:
        pilots = self.pilot_repository.find_by(**kargs)
        return pilots

    def find(self, id: int) -> Pilot:
        pilot = self.pilot_repository.find(id)
        return pilot

    def delete(self, id: int) -> None:
        pilot = self.pilot_repository.find(id)
        if pilot:
            self.pilot_repository.delete(pilot)