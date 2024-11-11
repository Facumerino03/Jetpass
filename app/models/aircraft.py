from dataclasses import dataclass
from datetime import date
from sqlalchemy import Enum, Time
from app import db
from app.models.enums import WakeTurbulenceCategoryEnum

@dataclass(init=True,eq=False)
class Aircraft(db.Model):
    """
    Class representing the aircrafts and its attributes
    """
    __tablename__ = "aircrafts"
    
    id:int = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    aircraft_identification:str = db.Column("aircraft_identification", db.String(7), unique=True, nullable=False)
    aircraft_type:str = db.Column("aircraft_type", db.String(4), nullable=False)
    wake_turbulence_category: str = db.Column("wake_turbulence_category", Enum(WakeTurbulenceCategoryEnum), nullable=False)
    equipment:str = db.Column("equipment", db.String(100), nullable=False)
    #TODO: validar con marshmallow donde debe ser en formato HHMM
    endurance:Time = db.Column("endurance", db.Time, nullable=False)
    passenger_capacity:str = db.Column("passenger_capacity", db.String(4), nullable=False, default='TBN')
    crew_capacity:int = db.Column("crew_capacity", db.Integer, nullable=False)
    #TODO: validar con marshmallow donde debe ser en formato N (de nudos) o K (kilometros) seguido de cuatro cifras
    max_speed:str = db.Column("max_speed", db.String, nullable=False)
    aircraft_colour_and_marking: str = db.Column("aircraft_colour_and_marking", db.String(100), nullable=False)
    
    
    def __eq__(self, plane: object) -> bool:
        return (
            self.id == plane.id and 
            self.aircraft_identification == plane.aircraft_identification and
            self.aircraft_type == plane.aircraft_type and
            self.wake_turbulence_category == plane.wake_turbulence_category and
            self.equipment == plane.equipment and
            self.endurance == plane.endurance and
            self.passenger_capacity == plane.passenger_capacity and
            self.crew_capacity == plane.crew_capacity and
            self.max_speed == plane.max_speed and
            self.aircraft_colour_and_marking == plane.aircraft_colour_and_marking
        )