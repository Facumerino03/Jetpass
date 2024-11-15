from typing import List
from app.models import Pilot
from app.repositories import PilotRepository

class PilotServices:
    '''
    Class that handles the CRUD of the pilots
    '''
    def __init__(self):
        self.pilot_repository = PilotRepository()

    def save(self, pilot: Pilot) -> Pilot:
        '''
        Saves the pilot
        
        param:
            pilot: Pilot
        return:
            Pilot
        '''
        return self.pilot_repository.save(pilot)

    def update(self, pilot: Pilot, id: int) -> Pilot:
        '''
        Updates the pilot
        
        param:
            pilot: Pilot
            id: int
        return:
            Pilot
        '''
        return self.pilot_repository.update(pilot, id)

    def find_all(self) -> List[Pilot]:
        '''
        Finds all the pilots
        
        return:
            List[Pilot]
        '''
        pilots = self.pilot_repository.find_all()
        return pilots

    def find_by(self, **kargs) -> List[Pilot]:
        '''
        Finds the pilots by the given arguments
        
        param:
            **kargs: dict
        return:
            List[Pilot]
        '''
        pilots = self.pilot_repository.find_by(**kargs)
        return pilots

    def find(self, id: int) -> Pilot:
        '''
        Finds the pilot by its id
        
        param:
            id: int
        return:
            Pilot
        '''
        pilot = self.pilot_repository.find(id)
        return pilot

    def delete(self, id: int) -> None:
        '''
        Deletes the pilot by its id
        
        param:
            id: int
        '''
        pilot = self.pilot_repository.find(id)
        if pilot:
            self.pilot_repository.delete(pilot)