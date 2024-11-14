from abc import ABC, abstractmethod
from datetime import datetime

class DateTimeFormatter(ABC):
    @abstractmethod
    def format(self, value: str) -> str:
        pass

class DepartureTimeFormatter(DateTimeFormatter):
    def format(self, value: str) -> str:
        try:
            time = datetime.strptime(value, '%H:%M:%S').time()
        except ValueError:
            time = datetime.strptime(value, '%H:%M').time()
        return time.strftime('%H%M')

class ElapsedTimeFormatter(DateTimeFormatter):
    def format(self, value: str) -> str:
        try:
            time = datetime.strptime(value, '%H:%M:%S').time()
        except ValueError:
            time = datetime.strptime(value, '%H:%M').time()
        return time.strftime('%H:%M')

class DepartureDateFormatter(DateTimeFormatter):
    def format(self, value: str) -> str:
        try:
            date = datetime.strptime(str(value), '%Y-%m-%d').date()
        except ValueError:
            date = datetime.strptime(str(value), '%d-%m-%Y').date()
        return date.strftime('%d-%m-%Y')

class FilingTimeFormatter(DateTimeFormatter):
    def format(self, value: str) -> str:
        try:
            time = datetime.strptime(value, '%H:%M:%S').time()
        except ValueError:
            time = datetime.strptime(value, '%H:%M').time()
        return time.strftime('%H%M')

class FormatterFactory:
    @staticmethod
    def get_formatter(field_type: str) -> DateTimeFormatter:
        formatters = {
            'departure_time': DepartureTimeFormatter(),
            'total_estimated_elapsed_time': ElapsedTimeFormatter(),
            'departure_date': DepartureDateFormatter(),
            'filing_time': FilingTimeFormatter()
        }
        return formatters[field_type]

class FlightPlanFormatterService:
    @staticmethod
    def format_for_response(flightplan_data: dict) -> dict:
        """Formatea los datos del plan de vuelo para la respuesta"""
        formatted_data = flightplan_data.copy()
        
        for field in ['departure_time', 'total_estimated_elapsed_time', 'departure_date', 'filing_time']:
            if field in formatted_data and formatted_data[field]:
                formatter = FormatterFactory.get_formatter(field)
                formatted_data[field] = formatter.format(formatted_data[field])
                
        return formatted_data