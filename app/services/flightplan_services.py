from app.repositories import FlightPlanRepository, PilotRepository, AircraftRepository, AirportRepository
from app.models import FlightPlan
from app.services.emergency_equipment_data_services import EmergencyEquipmentDataServices
from app.services.aerodrome_availability_service import AerodromeAvailabilityService
from app.services.aircraft_rules_services import AircraftRulesServices
from typing import List
from datetime import datetime
from app.services.entity_validation_service import EntityValidationService
from app.handlers.validation_result import ValidationResult
from app.services.speed_rules_service import SpeedRulesService

class FlightPlanServices:
    '''
    Class that handles the CRUD of the flight plans
    '''
    def __init__(self):
        self.flightplan_repository = FlightPlanRepository()
        self.emergency_equipment_data_services = EmergencyEquipmentDataServices()
        self.pilot_repository = PilotRepository()
        self.aircraft_repository = AircraftRepository()
        self.airport_repository = AirportRepository()
        self.aerodrome_availability_service = AerodromeAvailabilityService()
        self.aircraft_rules_services = AircraftRulesServices()
        self.entity_validation_service = EntityValidationService()
        self.speed_rules_service = SpeedRulesService()
    
    def save(self, flightplan_data: dict) -> FlightPlan:
        '''
        Saves the flight plan

        param:
            flightplan_data: dict
        return:
            FlightPlan
        '''
        validation_result = ValidationResult.success()
        
        # Validate existence of entities first
        entity_validation = self.entity_validation_service.validate_entities_exist(flightplan_data)
        if not entity_validation.is_valid:
            entity_validation.raise_if_invalid()
        
        # Validate departure aerodrome availability
        departure_validation = self.aerodrome_availability_service.check_departure_aerodrome_availability(
            flightplan_data['departure_aerodrome_id'],
            flightplan_data['departure_date'],
            flightplan_data['departure_time']
        )
        validation_result = validation_result.merge(departure_validation)
        
        # Validate aircraft rules
        capacity_validation = self.aircraft_rules_services.check_capacity(
            flightplan_data['aircraft_id'],
            flightplan_data['persons_on_board']
        )
        validation_result = validation_result.merge(capacity_validation)
        
        # Validate aircraft availability
        availability_validation = self.aircraft_rules_services.check_aircraft_availability(
            flightplan_data['aircraft_id'],
            flightplan_data['departure_date'],
            flightplan_data['departure_time'],
            flightplan_data['total_estimated_elapsed_time']
        )
        validation_result = validation_result.merge(availability_validation)

        # Validate max speed
        speed_validation = self.speed_rules_service.check_max_speed(
            flightplan_data['aircraft_id'],
            flightplan_data['cruising_speed']
        )
        validation_result = validation_result.merge(speed_validation)
        
        # If there are validation errors, raise an exception
        validation_result.raise_if_invalid()
        
        emergency_equipment_data = self.emergency_equipment_data_services.save(flightplan_data['emergency_equipment_data'])
        pilot = self.pilot_repository.find(flightplan_data['pilot_id'])
        aircraft = self.aircraft_repository.find(flightplan_data['aircraft_id'])
        departure_aerodrome = self.airport_repository.find(flightplan_data['departure_aerodrome_id'])
        destination_aerodrome = self.airport_repository.find(flightplan_data['destination_aerodrome_id'])
        first_alternative_aerodrome = self.airport_repository.find(flightplan_data['first_alternative_aerodrome_id'])
        second_alternative_aerodrome = self.airport_repository.find(flightplan_data['second_alternative_aerodrome_id'])

        flightplan = FlightPlan(
            submission_date=datetime.now(),
            priority=flightplan_data['priority'],
            address_to=flightplan_data['address_to'],
            filing_time=flightplan_data['filing_time'],
            originator=flightplan_data['originator'],
            message_type=flightplan_data['message_type'],
            aircraft_id=aircraft.id,
            flight_rules=flightplan_data['flight_rules'],
            flight_type=flightplan_data['flight_type'],
            number_of_aircraft=flightplan_data['number_of_aircraft'],
            pilot_id=pilot.id,
            departure_aerodrome_id=departure_aerodrome.id,
            departure_date=flightplan_data['departure_date'],
            departure_time=flightplan_data['departure_time'],
            cruising_speed=flightplan_data['cruising_speed'],
            cruising_level=flightplan_data['cruising_level'],
            route=flightplan_data['route'],
            destination_aerodrome_id=destination_aerodrome.id,
            total_estimated_elapsed_time=flightplan_data['total_estimated_elapsed_time'],
            first_alternative_aerodrome_id=first_alternative_aerodrome.id,
            second_alternative_aerodrome_id=second_alternative_aerodrome.id,
            other_information=flightplan_data['other_information'],
            persons_on_board=flightplan_data['persons_on_board'],
            emergency_equipment_data=emergency_equipment_data,
            remarks=flightplan_data['remarks'],
            remarks_details=flightplan_data['remarks_details'],
            filled_by_user_id=flightplan_data['filled_by_user_id'],
            document_signature_filename=flightplan_data['document_signature_filename']
        )
        
        flightplan = self.flightplan_repository.save(flightplan)
        return flightplan

    def find_all(self) -> List[FlightPlan]:
        '''
        Finds all the flight plans
        
        return:
            List[FlightPlan]
        '''
        return self.flightplan_repository.find_all()

    def find_by(self, **kargs) -> List[FlightPlan]:
        '''
        Finds the flight plans by the given arguments
        
        param:
            **kargs: dict
        return:
            List[FlightPlan]
        '''
        return self.flightplan_repository.find_by(**kargs)

    def find(self, id: int) -> FlightPlan:
        '''
        Finds the flight plan by its id
        
        param:
            id: int
        return:
            FlightPlan
        '''
        return self.flightplan_repository.find(id)

    def delete(self, id: int) -> None:
        '''
        Deletes the flight plan by its id
        
        param:
            id: int
        '''
        flightplan = self.flightplan_repository.find(id)
        if flightplan:
            self.flightplan_repository.delete(flightplan)