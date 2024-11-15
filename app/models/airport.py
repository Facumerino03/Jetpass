from dataclasses import dataclass
from sqlalchemy import Enum # type: ignore
from app import db
from app.models.enums import TrafficTypeAllowedEnum

@dataclass(init=True,eq=False)
class Airport(db.Model):
    '''
    Class representing the airports available for flight plans
    '''
    __tablename__ = "airports"
    
    id:int = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    name:str = db.Column("name", db.String(250), nullable=False)
    airport_code:str = db.Column("airport_code", db.String(4), unique=True, nullable=False)
    city:str = db.Column("city", db.String(100), nullable=False)
    country:str = db.Column("country", db.String(100), nullable=False)
    south_coordinates:float = db.Column("south_coordinates", db.Float, nullable=False)
    west_coordinates:float = db.Column("west_coordinates", db.Float, nullable=False)
    latitude:float = db.Column("latitude", db.Float, nullable=False)
    elevation:float = db.Column("elevation", db.Float, nullable=False)
    runway_length:float = db.Column("runway_length", db.Float, nullable=False)
    traffic_type_allowed:str = db.Column("traffic_type_allowed", Enum(TrafficTypeAllowedEnum), nullable=False)
    
    def __eq__(self, airport: object) -> bool:
        return (
            self.id == airport.id and
            self.name == airport.name and
            self.airport_code == airport.airport_code and
            self.city == airport.city and
            self.country == airport.country and
            self.south_coordinates == airport.south_coordinates and
            self.west_coordinates == airport.west_coordinates and
            self.latitude == airport.latitude and
            self.elevation == airport.elevation and
            self.runway_length == airport.runway_length and
            self.traffic_type_allowed == airport.traffic_type_allowed
        )