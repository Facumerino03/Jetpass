from datetime import datetime, timedelta, time
from app.repositories import FlightPlanRepository
from app.models import FlightPlan
from marshmallow import ValidationError
from app.handlers.validation_result import ValidationResult

class AerodromeAvailabilityService:
    def __init__(self):
        self.flightplan_repository = FlightPlanRepository()
    
    def check_departure_aerodrome_availability(self, departure_aerodrome_id: int, departure_date: str, departure_time: str) -> ValidationResult:
        try:
            parsed_date = datetime.strptime(departure_date, '%Y-%m-%d').date()
            parsed_time = datetime.strptime(departure_time, '%H%M').time()
            
            existing_plan = self.flightplan_repository.find_by_departure(departure_aerodrome_id, parsed_date, parsed_time)
            if existing_plan:
                return ValidationResult.failure(
                    'departure_aerodrome',
                    f"El aeródromo de salida {departure_aerodrome_id} no está disponible a las {departure_time}. "
                    f"Ya está asignado al plan de vuelo {existing_plan.id}"
                )
            
            return ValidationResult.success()
        except ValueError as e:
            return ValidationResult.failure(
                'departure_aerodrome',
                f"Error al procesar las fechas: {str(e)}"
            )
    def check_destination_aerodrome_availability(self, aerodrome_id: int, departure_date: str, departure_time: str, total_estimated_elapsed_time: str) -> ValidationResult:
        try:
            parsed_date = datetime.strptime(departure_date, '%Y-%m-%d').date()
            parsed_time = datetime.strptime(departure_time, '%H%M').time()
            parsed_elapsed = datetime.strptime(total_estimated_elapsed_time, '%H:%M').time()
            
            departure_datetime = datetime.combine(parsed_date, parsed_time)
            elapsed_time = timedelta(hours=parsed_elapsed.hour, minutes=parsed_elapsed.minute)
            estimated_arrival = departure_datetime + elapsed_time
            
            arrival_window_start = estimated_arrival - timedelta(minutes=30)
            arrival_window_end = estimated_arrival + timedelta(minutes=30)
            
            existing_plan = self.flightplan_repository.find_by_destination_in_timeframe(
                aerodrome_id, arrival_window_start, arrival_window_end
            )
            
            if existing_plan:
                return ValidationResult.failure(
                    'destination_aerodrome',
                    f"El aeródromo de destino {aerodrome_id} no está disponible en el horario estimado de llegada. "
                    f"Ya está asignado al plan de vuelo {existing_plan.id}"
                )
            
            return ValidationResult.success()
            
        except ValueError as e:
            return ValidationResult.failure(
                'destination_aerodrome',
                f"Error al procesar las fechas: {str(e)}"
            )
