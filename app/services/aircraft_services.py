from typing import List
from app.models import Aircraft
from app.repositories import AircraftRepository

class AircraftServices:
    '''
    Class that handles the CRUD of the aircrafts
    '''
    def __init__(self):
        self.aircraft_repository = AircraftRepository()

    def save(self, aircraft: Aircraft) -> Aircraft:
        '''
        Saves an aircraft
        
        param:
            aircraft: Aircraft
        return:
            Aircraft
        '''
        return self.aircraft_repository.save(aircraft)

    def update(self, aircraft: Aircraft, id: int) -> Aircraft:
        '''
        Updates an aircraft
        
        param:
            aircraft: Aircraft
            id: int
        return:
            Aircraft
        '''
        existing_aircraft = self.aircraft_repository.find(id)
        if existing_aircraft:
            existing_aircraft.aircraft_identification = aircraft.aircraft_identification
            existing_aircraft.aircraft_type = aircraft.aircraft_type
            existing_aircraft.wake_turbulence_category = aircraft.wake_turbulence_category
            existing_aircraft.equipment = aircraft.equipment
            existing_aircraft.endurance = aircraft.endurance
            existing_aircraft.passenger_capacity = aircraft.passenger_capacity
            existing_aircraft.crew_capacity = aircraft.crew_capacity
            existing_aircraft.max_speed = aircraft.max_speed
            existing_aircraft.aircraft_colour_and_marking = aircraft.aircraft_colour_and_marking
            return self.aircraft_repository.update(existing_aircraft)
        return None

    def find_all(self) -> List[Aircraft]:
        '''
        Finds all aircrafts
        
        return:
            List[Aircraft]
        '''
        aircrafts = self.aircraft_repository.find_all()
        return aircrafts

    def find_by(self, **kargs) -> List[Aircraft]:
        '''
        Finds aircrafts by the given arguments
        
        param:
            **kargs: dict
        return:
            List[Aircraft]
        '''
        aircrafts = self.aircraft_repository.find_by(**kargs)
        return aircrafts

    def find(self, id: int) -> Aircraft:
        '''
        Finds an aircraft by its id
        
        param:
            id: int
        return:
            Aircraft
        '''
        aircraft = self.aircraft_repository.find(id)
        return aircraft

    def delete(self, id: int) -> None:
        '''
        Deletes an aircraft by its id
        
        param:
            id: int
        '''
        aircraft = self.aircraft_repository.find(id)
        if aircraft:
            self.aircraft_repository.delete(aircraft)