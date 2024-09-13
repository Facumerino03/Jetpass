from app.repositories import FlightPlanRepository
from app.models import FlightPlan
from typing import List

class FlightPlanServices:
    """Clase que se encarga del CRUD de los planes de vuelo"""
    
    @staticmethod
    def save(flightplan: FlightPlan) -> FlightPlan:
        flightplan = FlightPlanRepository().save(flightplan)
        return flightplan
    
    @staticmethod
    def find_all() -> List['FlightPlan']:
        flightplans = FlightPlanRepository().find_all()
        return flightplans

    @staticmethod
    def find_by(**kargs) -> List['FlightPlan']:
        flightplans = FlightPlanRepository().find_by(**kargs)
        return flightplans
        
    @staticmethod
    def find(id:int) -> 'FlightPlan':
        flightplan = FlightPlanRepository().find(id)
        return flightplan
    
    @staticmethod
    def delete(flightplan:FlightPlan) -> None:
        FlightPlanRepository().delete(flightplan)