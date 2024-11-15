from app.services.speed_converter import SpeedConverter
from app.repositories import AircraftRepository
from app.handlers.validation_result import ValidationResult

class SpeedRulesService:
    '''
    Class that handles the speed rules
    '''
    
    def __init__(self):
        self.aircraft_repository = AircraftRepository()
        self.speed_converter = SpeedConverter()
    
    def check_max_speed(self, aircraft_id: int, cruising_speed: str) -> ValidationResult:
        '''
        Checks that the cruising speed does not exceed the maximum speed of the aircraft
        
        param:
            aircraft_id: int
            cruising_speed: str
        return:
            ValidationResult
        '''
        try:
            aircraft = self.aircraft_repository.find(aircraft_id)
            if not aircraft:
                return ValidationResult.failure(
                    'aircraft_speed',
                    f"No se encontró la aeronave con id {aircraft_id}"
                )
            
            try:
                cruising_speed_knots = self.speed_converter.convert_to_knots(cruising_speed)
                max_speed_knots = self.speed_converter.convert_to_knots(aircraft.max_speed)
                
                if cruising_speed_knots > max_speed_knots:
                    return ValidationResult.failure(
                        'aircraft_speed',
                        f"La velocidad de crucero ({cruising_speed}) excede la velocidad máxima "
                        f"de la aeronave ({aircraft.max_speed})"
                    )
                
                return ValidationResult.success()
                
            except ValueError as e:
                return ValidationResult.failure(
                    'aircraft_speed',
                    f"Error en el formato de velocidad: {str(e)}"
                )
            
        except Exception as e:
            return ValidationResult.failure(
                'aircraft_speed',
                f"Error al validar la velocidad: {str(e)}"
            )