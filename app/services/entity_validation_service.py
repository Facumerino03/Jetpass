from app.repositories import PilotRepository, AircraftRepository, AirportRepository
from app.handlers.validation_result import ValidationResult

class EntityValidationService:
    def __init__(self):
        self.pilot_repository = PilotRepository()
        self.aircraft_repository = AircraftRepository()
        self.airport_repository = AirportRepository()
    
    def validate_entities_exist(self, flightplan_data: dict) -> ValidationResult:
        """Valida que todas las entidades referenciadas existan"""
        errors = []
        
        # Validar piloto
        pilot = self.pilot_repository.find(flightplan_data['pilot_id'])
        if not pilot:
            errors.append(ValidationResult.failure(
                'pilot',
                f"No existe un piloto con id {flightplan_data['pilot_id']}"
            ))
        
        # Validar aeronave
        aircraft = self.aircraft_repository.find(flightplan_data['aircraft_id'])
        if not aircraft:
            errors.append(ValidationResult.failure(
                'aircraft',
                f"No existe una aeronave con id {flightplan_data['aircraft_id']}"
            ))
        
        # Validar aeródromos
        aerodromes = {
            'departure_aerodrome': flightplan_data['departure_aerodrome_id'],
            'destination_aerodrome': flightplan_data['destination_aerodrome_id'],
            'first_alternative_aerodrome': flightplan_data['first_alternative_aerodrome_id'],
            'second_alternative_aerodrome': flightplan_data['second_alternative_aerodrome_id']
        }
        
        for field, aerodrome_id in aerodromes.items():
            aerodrome = self.airport_repository.find(aerodrome_id)
            if not aerodrome:
                errors.append(ValidationResult.failure(
                    field,
                    f"No existe un aeródromo con id {aerodrome_id}"
                ))
        
        # Si hay errores, combinarlos
        if errors:
            result = errors[0]
            for error in errors[1:]:
                result = result.merge(error)
            return result
            
        return ValidationResult.success()