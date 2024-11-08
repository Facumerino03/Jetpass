from dataclasses import dataclass
from app import db

@dataclass(init=True,eq=False)
class Pilot(db.Model):
    """
    Class representing pilots in the flight plans
    """
    __tablename__ = "pilots"
    
    id:int = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    first_name:str = db.Column("first_name", db.String(100), nullable=False)
    last_name:str = db.Column("last_name", db.String(100), nullable=False)
    license_number:str = db.Column("license_number", db.String(100), unique=True, nullable=False)
    
    def __eq__(self, pilot: object) -> bool:
        return (
            self.id == pilot.id and
            self.first_name == pilot.first_name and
            self.last_name == pilot.last_name and
            self.license_number == pilot.license_number
        )