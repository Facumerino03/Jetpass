from app.repositories import PilotRepository, AircraftRepository, AirportRepository
from app.handlers.validation_result import ValidationResult

class EntityValidationService:
    def __init__(self):
        self.pilot_repository = PilotRepository()
        self.aircraft_repository = AircraftRepository()
        self.airport_repository = AirportRepository()
    
    def validate_entities_exist(self, flightplan_data: dict) -> ValidationResult:
        """Valida que todas las entidades referenciadas existan"""
        validation_result = ValidationResult.success()
        
        # Validar piloto
        if not self.pilot_repository.find(flightplan_data['pilot_id']):
            validation_result.add_error(
                'pilot',
                f"No existe un piloto con id {flightplan_data['pilot_id']}"
            )
        
        # Validar aeronave
        if not self.aircraft_repository.find(flightplan_data['aircraft_id']):
            validation_result.add_error(
                'aircraft',
                f"No existe una aeronave con id {flightplan_data['aircraft_id']}"
            )
        
        # Validar aeródromos
        aerodromes = {
            'departure_aerodrome': flightplan_data['departure_aerodrome_id'],
            'destination_aerodrome': flightplan_data['destination_aerodrome_id'],
            'first_alternative_aerodrome': flightplan_data['first_alternative_aerodrome_id'],
            'second_alternative_aerodrome': flightplan_data['second_alternative_aerodrome_id']
        }
        
        for field, aerodrome_id in aerodromes.items():
            if not self.airport_repository.find(aerodrome_id):
                validation_result.add_error(
                    field,
                    f"No existe un aeródromo con id {aerodrome_id}"
                )
        
        return validation_result