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
        Finds a flight plan by departure aerodrome, date and time.
        
        The generated SQL query would be equivalent to:
        
        SELECT * FROM flight_plans 
        WHERE departure_aerodrome_id = :aerodrome_id 
        AND departure_date = :departure_date 
        AND departure_time = :departure_time 
        LIMIT 1
        
        This query is used to verify if there is another flight plan
        scheduled for the same aerodrome at the same departure date and time,
        which is not allowed by business rules.
        
        Args:
            aerodrome_id (int): Departure aerodrome ID
            departure_date (datetime.date): Departure date
            departure_time (datetime.time): Departure time
        
        Returns:
            FlightPlan: The found flight plan or None if none exists
        
        Example:
            >>> repo.find_by_departure(1, date(2024,3,20), time(14,30))
            <FlightPlan id=123>
        '''
        return FlightPlan.query.filter(
            FlightPlan.departure_aerodrome_id == aerodrome_id,
            FlightPlan.departure_date == departure_date,
            FlightPlan.departure_time == departure_time
    ).first()
    
    def find_by_destination_in_timeframe(self, aerodrome_id: int, arrival_window_start: datetime, arrival_window_end: datetime) -> list[FlightPlan]:
        '''
        Finds flight plans that have the given aerodrome as destination or alternative 
        within a specific time window.
        
        The generated SQL query would be equivalent to:
        
        SELECT * FROM flight_plans 
        WHERE (destination_aerodrome_id = :aerodrome_id 
               OR first_alternative_aerodrome_id = :aerodrome_id 
               OR second_alternative_aerodrome_id = :aerodrome_id)
        AND departure_date = :arrival_window_start_date
        AND CAST(departure_time AS TIME) BETWEEN :arrival_window_start_time AND :arrival_window_end_time
        
        This query is used to check if there are other flight plans that might be 
        arriving at the same aerodrome within a ±30-minute window of the estimated arrival time.
        
        Args:
            aerodrome_id (int): ID of the aerodrome to check
            arrival_window_start (datetime): Start of the arrival time window
            arrival_window_end (datetime): End of the arrival time window
        
        Returns:
            list[FlightPlan]: List of flight plans found in the time window
        
        Example:
            >>> start = datetime(2024, 3, 20, 14, 0)
            >>> end = datetime(2024, 3, 20, 15, 0)
            >>> repo.find_by_destination_in_timeframe(1, start, end)
            [<FlightPlan id=123>, <FlightPlan id=124>]
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
        Finds if an aircraft is already scheduled for a flight plan within the given timeframe.
        
        The generated SQL query would be equivalent to:
        
        SELECT * FROM flight_plans 
        WHERE aircraft_id = :aircraft_id
        AND (departure_date + departure_time) >= :start_time
        AND (departure_date + departure_time + total_estimated_elapsed_time) <= :end_time
        LIMIT 1
        
        This query checks if the aircraft is already assigned to another flight plan
        that overlaps with the requested time period. It considers both the departure
        time and the estimated flight duration to determine availability.
        
        Args:
            aircraft_id (int): ID of the aircraft to check
            start_time (datetime): Start of the requested time period
            end_time (datetime): End of the requested time period
        
        Returns:
            FlightPlan: The conflicting flight plan if found, None otherwise
        
        Example:
            >>> start = datetime(2024, 3, 20, 14, 0)
            >>> end = datetime(2024, 3, 20, 18, 0)
            >>> repo.find_by_aircraft_in_timeframe(1, start, end)
            <FlightPlan id=123>
        '''
        return FlightPlan.query.filter(
        FlightPlan.aircraft_id == aircraft_id,
        FlightPlan.departure_date + FlightPlan.departure_time >= start_time,
        FlightPlan.departure_date + FlightPlan.departure_time + FlightPlan.total_estimated_elapsed_time <= end_time
    ).first()