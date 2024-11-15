from datetime import datetime, timedelta
from app.repositories import AircraftRepository, FlightPlanRepository
from app.handlers.validation_result import ValidationResult

class AircraftRulesServices:
    '''
    Class that checks the capacity and availability of the aircraft
    '''
    def __init__(self):
        self.aircraft_repository = AircraftRepository()
        self.flightplan_repository = FlightPlanRepository()
    
    def check_capacity(self, aircraft_id: int, persons_on_board: int) -> ValidationResult:
        '''
        Checks if the number of people does not exceed the aircraft's capacity
        
        param:
            aircraft_id: int
            persons_on_board: int
        return:
            ValidationResult
        '''
        aircraft = self.aircraft_repository.find(aircraft_id)
        
        try:
            total_capacity = int(aircraft.passenger_capacity) + aircraft.crew_capacity
            
            if persons_on_board > total_capacity:
                return ValidationResult.failure(
                    'aircraft_capacity',
                    f"Total de personas ({persons_on_board}) excede la capacidad de la aeronave "
                    f"(pasajeros: {aircraft.passenger_capacity}, tripulación: {aircraft.crew_capacity})"
                )
            
            return ValidationResult.success()
        except ValueError:
            return ValidationResult.failure(
                'aircraft_capacity',
                f"Error en la configuración de capacidad de la aeronave. "
                f"Capacidad de pasajeros: {aircraft.passenger_capacity}"
            )
    
    def check_aircraft_availability(self, aircraft_id: int, departure_date: str, departure_time: str, total_estimated_elapsed_time: str) -> ValidationResult:
        '''
        Checks if the aircraft is available in the requested time period
        
        param:
            aircraft_id: int
            departure_date: str
            departure_time: str
            total_estimated_elapsed_time: str
        return:
            ValidationResult
        '''
        try:
            parsed_date = datetime.strptime(departure_date, '%Y-%m-%d').date()
            parsed_time = datetime.strptime(departure_time, '%H%M').time()
            parsed_elapsed = datetime.strptime(total_estimated_elapsed_time, '%H:%M').time()
            
            departure_datetime = datetime.combine(parsed_date, parsed_time)
            elapsed_time = timedelta(hours=parsed_elapsed.hour, minutes=parsed_elapsed.minute)
            estimated_arrival = departure_datetime + elapsed_time
            
            existing_plan = self.flightplan_repository.find_by_aircraft_in_timeframe(
                aircraft_id, 
                departure_datetime, 
                estimated_arrival
            )
            
            if existing_plan:
                return ValidationResult.failure(
                    'aircraft_availability',
                    f"La aeronave {aircraft_id} no está disponible en el período solicitado. "
                    f"Ya está asignada al plan de vuelo {existing_plan.id}"
                )
            
            return ValidationResult.success()
            
        except ValueError as e:
            return ValidationResult.failure(
                'aircraft_availability',
                f"Error al procesar las fechas y tiempos: {str(e)}"
            )