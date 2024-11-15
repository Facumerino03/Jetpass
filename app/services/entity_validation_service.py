from app.repositories import PilotRepository, AircraftRepository, AirportRepository
from marshmallow import ValidationError

class EntityValidationService:
    def __init__(self):
        self.pilot_repository = PilotRepository()
        self.aircraft_repository = AircraftRepository()
        self.airport_repository = AirportRepository()
    
    def validate_entities_exist(self, flightplan_data: dict) -> None:
        """Valida que todas las entidades referenciadas existan"""
        errors = {}
        
        # Validar piloto
        if not self.pilot_repository.find(flightplan_data['pilot_id']):
            errors['pilot_id'] = f"No existe un piloto con id {flightplan_data['pilot_id']}"
        
        # Validar aeronave
        if not self.aircraft_repository.find(flightplan_data['aircraft_id']):
            errors['aircraft_id'] = f"No existe una aeronave con id {flightplan_data['aircraft_id']}"
        
        # Validar aeródromos
        aerodromes = {
            'departure_aerodrome_id': flightplan_data['departure_aerodrome_id'],
            'destination_aerodrome_id': flightplan_data['destination_aerodrome_id'],
            'first_alternative_aerodrome_id': flightplan_data['first_alternative_aerodrome_id'],
            'second_alternative_aerodrome_id': flightplan_data['second_alternative_aerodrome_id']
        }
        
        for field, aerodrome_id in aerodromes.items():
            if not self.airport_repository.find(aerodrome_id):
                errors[field] = f"No existe un aeródromo con id {aerodrome_id}"
        
        if errors:
            raise ValidationError(errors)