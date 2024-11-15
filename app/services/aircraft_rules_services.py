from datetime import datetime, timedelta
from marshmallow import ValidationError
from app.repositories import AircraftRepository, FlightPlanRepository

class AircraftRulesServices:
    def __init__(self):
        self.aircraft_repository = AircraftRepository()
        self.flightplan_repository = FlightPlanRepository()
    
    def check_capacity(self, aircraft_id: int, persons_on_board: int) -> None:
        """Verifica que la cantidad de personas no exceda la capacidad de la aeronave"""
        aircraft = self.aircraft_repository.find(aircraft_id)
        
        try:
            total_capacity = int(aircraft.passenger_capacity) + aircraft.crew_capacity
            
            if persons_on_board > total_capacity:
                raise ValidationError(
                    f"Total de personas ({persons_on_board}) excede la capacidad de la aeronave "
                    f"(pasajeros: {aircraft.passenger_capacity}, tripulación: {aircraft.crew_capacity})"
                )
        except ValueError:
            raise ValidationError(
                f"Error en la configuración de capacidad de la aeronave. "
                f"Capacidad de pasajeros: {aircraft.passenger_capacity}"
            )
    
    def check_aircraft_availability(self, aircraft_id: int, departure_date: str, departure_time: str, total_estimated_elapsed_time: str) -> None:
        """
        Verifica si la aeronave está disponible en el período de tiempo solicitado
        """
        # Parsear las fechas y tiempos
        parsed_date = datetime.strptime(departure_date, '%Y-%m-%d').date()
        parsed_time = datetime.strptime(departure_time, '%H%M').time()
        parsed_elapsed = datetime.strptime(total_estimated_elapsed_time, '%H:%M').time()
        
        # Calcular ventana de tiempo del vuelo
        departure_datetime = datetime.combine(parsed_date, parsed_time)
        elapsed_time = timedelta(hours=parsed_elapsed.hour, minutes=parsed_elapsed.minute)
        estimated_arrival = departure_datetime + elapsed_time
        
        # Buscar planes de vuelo que usen esta aeronave en ese período
        existing_plan = self.flightplan_repository.find_by_aircraft_in_timeframe(
            aircraft_id, 
            departure_datetime, 
            estimated_arrival
        )
        
        if existing_plan:
            raise ValidationError(
                f"La aeronave {aircraft_id} no está disponible en el período solicitado. "
                f"Ya está asignada al plan de vuelo {existing_plan.id}"
            )