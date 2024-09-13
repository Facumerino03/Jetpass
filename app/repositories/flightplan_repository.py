from typing import List
from app.models import FlightPlan
from app import db
from repositories import AbstractRepository

class FlightPlanRepository(AbstractRepository):
    
    def save(self, flightplan:FlightPlan) -> FlightPlan:
        db.session.add(flightplan)
        db.session.commit()
        return flightplan
      
    def find_all(self) -> List['FlightPlan']:
        return FlightPlan.query.all()

    def find_by(self, **kargs) -> List['FlightPlan']:
        return FlightPlan.query.filter_by(**kargs).all()
        
    def find(self, id:int) -> 'FlightPlan':
        return FlightPlan.query.get(id)
    
    def delete(self, flightplan:FlightPlan) -> None:
        db.session.delete(flightplan)
        db.session.commit()