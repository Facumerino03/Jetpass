from dataclasses import dataclass
from turtle import st
from app import db

@dataclass(init=True,eq=False)
class FlightPlan(db.Model):
    """
    Clase que representa un usuario del sistema con distintos perfiles.
    """
    __tablename__ = "flight_plans"
    id:int = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    pilot:str = db.Column("pilot", db.String(100), nullable=False)
    requested_aerodrome:str = db.Column("requested_aerodrome", db.String(100), nullable=False)
    departure_aerodrome:str = db.Column("departure_aerodrome", db.String(100), nullable=False)
    first_alternative_aerodrome:str = db.Column("first_alternative_aerodrome", db.String(100), nullable=False)
    second_alternative_aerodrome:str = db.Column("second_alternative_aerodrome", db.String(100), nullable=False)
    destination_aerodrome:str = db.Column("destination_aerodrome", db.String(100), nullable=False)
    aircraft_registration:str = db.Column("aircraft_registration", db.String(100), nullable=False)
    aircraft_type:str = db.Column("aircraft_type", db.String(100), nullable=False)
    start_date = db.Column("start_date", db.DateTime(100), nullable=False)
    start_time_utc = db.Column("start_time_utc", db.DateTime(100), nullable=False)
    end_date = db.Column("end_date", db.DateTime(100), nullable=False)
    end_time_utc = db.Column("end_time_utc", db.DateTime(100), nullable=False)
    reason:str = db.Column("reason", db.String(100), nullable=False)
    observations:str = db.Column("observations", db.String(100), nullable=False)
    document_submission_date = db.Column("document_submission_date", db.DateTime(100), nullable=False)
    document_submission_time = db.Column("document_submission_time", db.DateTime(100), nullable=False)
    
    
    def __eq__(self, flightplan: object) -> bool:
        return self.id == flightplan.id and self.pilot == flightplan.pilot and self.requested_aerodrome == flightplan.requested_aerodrome and self.departure_aerodrome == flightplan.departure_aerodrome and self.first_alternative_aerodrome == flightplan.first_alternative_aerodrome and self.second_alternative_aerodrome == flightplan.second_alternative_aerodrome and self.destination_aerodrome == flightplan.destination_aerodrome and self.aircraft_registration == flightplan.aircraft_registration and self.aircraft_type == flightplan.aircraft_type and self.start_date == flightplan.start_date and self.start_time_utc == flightplan.start_time_utc and self.end_date == flightplan.end_date and self.end_time_utc == flightplan.end_time_utc and self.reason == flightplan.reason and self.observations == flightplan.observations and self.document_submission_date == flightplan.document_submission_date and self.document_submission_time == flightplan.document_submission_time