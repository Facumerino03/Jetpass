from typing import List
from app.models import FlightPlan
from app import db

class FlightPlanRepository:
    
    @staticmethod
    def save(flightplan:FlightPlan) -> FlightPlan:
        db.session.add(flightplan)
        db.session.commit()

        return flightplan
   
    @staticmethod   
    def find_all() -> List['FlightPlan']:
        return FlightPlan.query.all()

    @staticmethod
    def find_by(**kargs) -> List['FlightPlan']:
        return FlightPlan.query.filter_by(**kargs).all()
        
    @staticmethod
    def find(id:int) -> 'FlightPlan':
        return FlightPlan.query.get(id)
    
    @staticmethod
    def delete(flightplan:FlightPlan) -> None:
        db.session.delete(flightplan)
        db.session.commit()