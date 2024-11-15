from datetime import datetime, timedelta, time
from app.repositories import FlightPlanRepository
from app.models import FlightPlan

class AerodromeAvailabilityService:
    def __init__(self):
        self.flightplan_repository = FlightPlanRepository()
    
    def check_departure_aerodrome_availability(self, departure_aerodrome_id: int, departure_date: str, departure_time: str) -> FlightPlan:
        """
        Verifica si hay otro plan de vuelo usando el mismo aeródromo de salida en la misma fecha y hora
        """
        parsed_date = datetime.strptime(departure_date, '%Y-%m-%d').date()
        parsed_time = datetime.strptime(departure_time, '%H%M').time()
        
        existing_plan = self.flightplan_repository.find_by_departure(departure_aerodrome_id, parsed_date, parsed_time)
        return existing_plan
    
    def check_destination_aerodrome_availability(self, aerodrome_id: int, departure_date: str, departure_time: str, total_estimated_elapsed_time: str) -> FlightPlan:
        """
        Verifica si hay otro plan de vuelo usando el aeródromo como destino en el lapso de tiempo estimado
        """
        parsed_date = datetime.strptime(departure_date, '%Y-%m-%d').date()
        parsed_time = datetime.strptime(departure_time, '%H%M').time()
        parsed_elapsed = datetime.strptime(total_estimated_elapsed_time, '%H:%M').time()
        
        departure_datetime = datetime.combine(parsed_date, parsed_time)
        elapsed_time = timedelta(hours=parsed_elapsed.hour, minutes=parsed_elapsed.minute)
        estimated_arrival = departure_datetime + elapsed_time
        
        arrival_window_start = estimated_arrival - timedelta(minutes=30)
        arrival_window_end = estimated_arrival + timedelta(minutes=30)
        
        existing_plan = self.flightplan_repository.find_by_destination_in_timeframe(aerodrome_id, arrival_window_start, arrival_window_end)
        return existing_plan