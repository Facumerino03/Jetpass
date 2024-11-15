from app.repositories import FlightPlanRepository, PilotRepository, AircraftRepository, AirportRepository
from app.models import FlightPlan, Pilot, Aircraft, Airport
from app.services.emergency_equipment_data_services import EmergencyEquipmentDataServices
from app.services.aerodrome_availability_service import AerodromeAvailabilityService
from app.services.aircraft_rules_services import AircraftRulesServices
from typing import List
from datetime import datetime, timedelta
from marshmallow import ValidationError
from app.services.entity_validation_service import EntityValidationService

class FlightPlanServices:
    """Clase que se encarga del CRUD de los planes de vuelo"""
    
    def __init__(self):
        self.flightplan_repository = FlightPlanRepository()
        self.emergency_equipment_data_services = EmergencyEquipmentDataServices()
        self.pilot_repository = PilotRepository()
        self.aircraft_repository = AircraftRepository()
        self.airport_repository = AirportRepository()
        self.aerodrome_availability_service = AerodromeAvailabilityService()
        self.aircraft_rules_services = AircraftRulesServices()
        self.entity_validation_service = EntityValidationService()

    def save(self, flightplan_data: dict) -> FlightPlan:
        
        # Validar existencia de entidades
        self.entity_validation_service.validate_entities_exist(flightplan_data)
        
        # Validar disponibilidad de aeródromos
        self.aerodrome_availability_service.check_departure_aerodrome_availability(
            flightplan_data['departure_aerodrome_id'],
            flightplan_data['departure_date'],
            flightplan_data['departure_time']
        )
        
        # Validar aeródromos de destino y alternativos
        aerodromes = [
            flightplan_data['destination_aerodrome_id'],
            flightplan_data['first_alternative_aerodrome_id'],
            flightplan_data['second_alternative_aerodrome_id']
        ]
        self.aerodrome_availability_service.check_alternative_aerodromes_availability(
            aerodromes,
            flightplan_data['departure_date'],
            flightplan_data['departure_time'],
            flightplan_data['total_estimated_elapsed_time']
        )

        # Validar reglas de aeronave
        self.aircraft_rules_services.check_capacity(
            flightplan_data['aircraft_id'],
            flightplan_data['persons_on_board']
        )
        
        self.aircraft_rules_services.check_aircraft_availability(
            flightplan_data['aircraft_id'],
            flightplan_data['departure_date'],
            flightplan_data['departure_time'],
            flightplan_data['total_estimated_elapsed_time']
        )

        # Crear los modelos relacionados
        emergency_equipment_data = self.emergency_equipment_data_services.save(flightplan_data['emergency_equipment_data'])
        pilot = self.pilot_repository.find(flightplan_data['pilot_id'])
        aircraft = self.aircraft_repository.find(flightplan_data['aircraft_id'])
        departure_aerodrome = self.airport_repository.find(flightplan_data['departure_aerodrome_id'])
        destination_aerodrome = self.airport_repository.find(flightplan_data['destination_aerodrome_id'])
        first_alternative_aerodrome = self.airport_repository.find(flightplan_data['first_alternative_aerodrome_id'])
        second_alternative_aerodrome = self.airport_repository.find(flightplan_data['second_alternative_aerodrome_id'])

        # Crear el FlightPlan
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
        
        # Guardar el FlightPlan
        flightplan = self.flightplan_repository.save(flightplan)
        return flightplan

    def find_all(self) -> List[FlightPlan]:
        return self.flightplan_repository.find_all()

    def find_by(self, **kargs) -> List[FlightPlan]:
        return self.flightplan_repository.find_by(**kargs)

    def find(self, id: int) -> FlightPlan:
        return self.flightplan_repository.find(id)

    def delete(self, id: int) -> None:
        flightplan = self.flightplan_repository.find(id)
        if flightplan:
            self.flightplan_repository.delete(flightplan)