import logging
from typing import List
from app.models import FlightPlan
from app import db
from app.repositories.base_repository import CreateAbstractRepository, ReadAbstractRepository, UpdateAbstractRepository, DeleteAbstractRepository

class FlightPlanRepository(CreateAbstractRepository, ReadAbstractRepository, UpdateAbstractRepository, DeleteAbstractRepository):
    
    def save(self, flightplan: FlightPlan) -> FlightPlan:
        db.session.add(flightplan)
        db.session.commit()
        return flightplan
    
    def find(self, id: int) -> FlightPlan:
        result = None
        if id is not None:
            try:
                result = FlightPlan.query.get(id)
            except Exception as e:
                logging.error(f'error getting flight plan by id: {id}, {e}') 
        return result
    
    def find_all(self) -> List[FlightPlan]:
        return FlightPlan.query.all()
    
    def find_by(self, **kargs) -> List[FlightPlan]:
        return FlightPlan.query.filter_by(**kargs).all()
    
    def delete(self, flightplan: FlightPlan) -> None:
        existing_flightplan = self.find(flightplan.id)
        if existing_flightplan:
            db.session.delete(existing_flightplan)
            db.session.commit()
        else:
            logging.error(f'error deleting flight plan by id: {flightplan.id}')
    
    def update(self, flightplan: FlightPlan) -> FlightPlan:
        existing_flightplan = self.find(flightplan.id)
        
        if existing_flightplan is None:
            return None
        
        existing_flightplan.submission_date = flightplan.submission_date
        existing_flightplan.priority = flightplan.priority
        existing_flightplan.address_to = flightplan.address_to
        existing_flightplan.filing_time = flightplan.filing_time
        existing_flightplan.originator = flightplan.originator
        existing_flightplan.message_type = flightplan.message_type
        existing_flightplan.aircraft_id = flightplan.aircraft_id
        existing_flightplan.flight_rules = flightplan.flight_rules
        existing_flightplan.flight_type = flightplan.flight_type
        existing_flightplan.number_of_aircraft = flightplan.number_of_aircraft
        existing_flightplan.pilot_id = flightplan.pilot_id
        existing_flightplan.departure_aerodrome_id = flightplan.departure_aerodrome_id
        existing_flightplan.departure_time = flightplan.departure_time
        existing_flightplan.cruising_speed = flightplan.cruising_speed
        existing_flightplan.cruising_level = flightplan.cruising_level
        existing_flightplan.route = flightplan.route
        existing_flightplan.destination_aerodrome_id = flightplan.destination_aerodrome_id
        existing_flightplan.total_estimated_elapsed_time = flightplan.total_estimated_elapsed_time
        existing_flightplan.first_alternative_aerodrome_id = flightplan.first_alternative_aerodrome_id
        existing_flightplan.second_alternative_aerodrome_id = flightplan.second_alternative_aerodrome_id
        existing_flightplan.other_information = flightplan.other_information
        existing_flightplan.persons_on_board = flightplan.persons_on_board
        existing_flightplan.emergency_equipment_data_id = flightplan.emergency_equipment_data_id
        existing_flightplan.remarks = flightplan.remarks
        existing_flightplan.remarks_details = flightplan.remarks_details
        existing_flightplan.filled_by_user_id = flightplan.filled_by_user_id
        existing_flightplan.document_signature_filename = flightplan.document_signature_filename
        
        db.session.commit()
        return existing_flightplan