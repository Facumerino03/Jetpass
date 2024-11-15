from datetime import datetime
from sqlalchemy import and_, or_, func, Time # type: ignore
import logging
from typing import List
from app.models import FlightPlan
from app import db
from app.repositories.base_repository import CreateAbstractRepository, ReadAbstractRepository, DeleteAbstractRepository

class FlightPlanRepository(CreateAbstractRepository, ReadAbstractRepository, DeleteAbstractRepository):
    '''
    Class representing the flight plans repository (interacts with the database)
    '''
    def save(self, flightplan: FlightPlan) -> FlightPlan:
        '''
        Saves a flight plan to the database
        param:
            flightplan: FlightPlan
        return:
            FlightPlan: The saved flight plan
        '''
        db.session.add(flightplan)
        db.session.commit()
        return flightplan
    
    def find(self, id: int) -> FlightPlan:
        '''
        Finds a flight plan by its id
        param:
            id: int
        return:
            FlightPlan: The flight plan found
        '''
        result = None
        if id is not None:
            try:
                result = FlightPlan.query.get(id)
            except Exception as e:
                logging.error(f'error getting flight plan by id: {id}, {e}') 
        return result
    
    def find_all(self) -> List[FlightPlan]:
        '''
        Finds all flight plans
        return:
            List[FlightPlan]: The list of flight plans found
        '''
        return FlightPlan.query.all()
    
    def find_by(self, **kargs) -> List[FlightPlan]:
        '''
        Finds flight plans by a given criteria
        param:
            kargs: dict
        return:
            List[FlightPlan]: The list of flight plans found
        '''
        return FlightPlan.query.filter_by(**kargs).all()
    
    def delete(self, flightplan: FlightPlan) -> None:
        '''
        Deletes a flight plan from the database
        param:
            flightplan: FlightPlan
        '''
        existing_flightplan = self.find(flightplan.id)
        if existing_flightplan:
            db.session.delete(existing_flightplan)
            db.session.commit()
        else:
            logging.error(f'error deleting flight plan by id: {flightplan.id}')

    def find_by_departure(self, aerodrome_id: int, departure_date: datetime.date, departure_time: datetime.time) -> FlightPlan:
        '''
        Finds a flight plan by its departure aerodrome id, departure date and departure time
        param:
            aerodrome_id: int
            departure_date: datetime.date
            departure_time: datetime.time
        return:
            FlightPlan: The flight plan found
        '''
        return FlightPlan.query.filter(
            FlightPlan.departure_aerodrome_id == aerodrome_id,
            FlightPlan.departure_date == departure_date,
            FlightPlan.departure_time == departure_time
    ).first()
    
    def find_by_destination_in_timeframe(self, aerodrome_id: int, arrival_window_start: datetime, arrival_window_end: datetime) -> list[FlightPlan]:
        '''
        Finds flight plans by its destination aerodrome id, arrival window start and arrival window end
        param:
            aerodrome_id: int
            arrival_window_start: datetime
            arrival_window_end: datetime
        return:
            list[FlightPlan]: The list of flight plans found
        '''
        return FlightPlan.query.filter(
            or_(
                FlightPlan.destination_aerodrome_id == aerodrome_id,
                FlightPlan.first_alternative_aerodrome_id == aerodrome_id,
                FlightPlan.second_alternative_aerodrome_id == aerodrome_id
            ),
            FlightPlan.departure_date == arrival_window_start.date(),
            and_(
                func.cast(FlightPlan.departure_time, Time) <= arrival_window_end.time(),
                func.cast(FlightPlan.departure_time, Time) >= arrival_window_start.time()
            )
        ).all()

    def find_by_aircraft_in_timeframe(self, aircraft_id: int, start_time: datetime, end_time: datetime) -> FlightPlan:
        '''
        Finds flight plans by its aircraft id, start time and end time
        param:
            aircraft_id: int
            start_time: datetime
            end_time: datetime
        return:
            FlightPlan: The flight plan found
        '''
        return FlightPlan.query.filter(
        FlightPlan.aircraft_id == aircraft_id,
        FlightPlan.departure_date + FlightPlan.departure_time >= start_time,
        FlightPlan.departure_date + FlightPlan.departure_time + FlightPlan.total_estimated_elapsed_time <= end_time
    ).first()