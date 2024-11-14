from dataclasses import dataclass
from datetime import date
from sqlalchemy import Enum, Time
from app import db
from app.models.enums import FlightRulesEnum, FlightTypeEnum

@dataclass(init=True,eq=False)
class FlightPlan(db.Model):
    """
    Class representing the flight plans and its attributes
    """
    __tablename__ = "flight_plans"
    
    id:int = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    submission_date:date = db.Column("submission_date", db.DateTime, nullable=False)
    priority:str = db.Column("priority", db.String(100), nullable=False, default="FF")
    address_to:str = db.Column("address_to", db.String(100), nullable=False)
    filing_time:Time = db.Column("filing_time", db.Time, nullable=False)
    originator:str = db.Column("originator", db.String(8), nullable=False)
    message_type:str = db.Column("message_type", db.String(100), nullable=False, default="FPL")
    aircraft_id = db.Column("aircraft_id", db.Integer, db.ForeignKey("aircrafts.id"))
    flight_rules = db.Column("flight_rules", Enum(FlightRulesEnum), nullable=False)
    flight_type = db.Column("flight_type", Enum(FlightTypeEnum), nullable=False)
    number_of_aircraft:int = db.Column("number_of_aircraft", db.Integer, nullable=False)
    pilot_id:int = db.Column("pilot_id", db.Integer, db.ForeignKey("pilots.id"))
    departure_aerodrome_id:int = db.Column("departure_aerodrome_id", db.Integer, db.ForeignKey("airports.id"))
    departure_date = db.Column("departure_date", db.DateTime, nullable=False)
    departure_time: Time = db.Column("departure_time", db.Time, nullable=False)
    cruising_speed = db.Column("cruising_speed", db.String(5), nullable=False)
    cruising_level = db.Column("cruising_level", db.String(5), nullable=False)
    route:str = db.Column("route", db.String(100), nullable=False)
    destination_aerodrome_id:int = db.Column("destination_aerodrome_id", db.Integer, db.ForeignKey("airports.id"))
    total_estimated_elapsed_time = db.Column("total_estimated_elapsed_time", db.Time, nullable=False)
    first_alternative_aerodrome_id:int = db.Column("first_alternative_aerodrome_id", db.Integer, db.ForeignKey("airports.id"))
    second_alternative_aerodrome_id:int = db.Column("second_alternative_aerodrome_id", db.Integer, db.ForeignKey("airports.id"))
    other_information:str = db.Column("other_information", db.String(256), nullable=False)
    persons_on_board:int = db.Column("persons_on_board", db.Integer, nullable=False)
    emergency_equipment_data_id: int = db.Column("emergency_equipment_data_id", db.Integer, db.ForeignKey('emergency_equipment_data.id'))
    emergency_equipment_data = db.relationship('EmergencyEquipmentData', back_populates='flight_plan', cascade='all, delete-orphan', uselist=False, single_parent=True)
    remarks:bool = db.Column("remarks", db.Boolean, nullable=False, default=False)
    remarks_details:str = db.Column("remarks_details", db.String(256), nullable=False)
    pilot_id:int = db.Column("pilot_id", db.Integer, db.ForeignKey("pilots.id"))
    filled_by_user_id:int = db.Column("filled_by_user_id", db.Integer, db.ForeignKey("users.id"))
    document_signature_filename:str = db.Column("document_signature_filename", db.String(100), nullable=False)
    
    
    def __eq__(self, flight_plan: object) -> bool:
        return (
            self.id == flight_plan.id and
            self.submission_date == flight_plan.submission_date and
            self.priority == flight_plan.priority and
            self.address_to == flight_plan.address_to and
            self.filing_time == flight_plan.filing_time and
            self.originator == flight_plan.originator and
            self.message_type == flight_plan.message_type and
            self.aircraft_id == flight_plan.aircraft_id and
            self.flight_rules == flight_plan.flight_rules and
            self.flight_type == flight_plan.flight_type and
            self.number_of_aircraft == flight_plan.number_of_aircraft and
            self.pilot_id == flight_plan.pilot_id and
            self.departure_aerodrome_id == flight_plan.departure_aerodrome_id and
            self.departure_date == flight_plan.departure_date and
            self.departure_time == flight_plan.departure_time and
            self.cruising_speed == flight_plan.cruising_speed and
            self.cruising_level == flight_plan.cruising_level and
            self.route == flight_plan.route and
            self.destination_aerodrome_id == flight_plan.destination_aerodrome_id and
            self.total_estimated_elapsed_time == flight_plan.total_estimated_elapsed_time and
            self.first_alternative_aerodrome_id == flight_plan.first_alternative_aerodrome_id and
            self.second_alternative_aerodrome_id == flight_plan.second_alternative_aerodrome_id and
            self.other_information == flight_plan.other_information and
            self.persons_on_board == flight_plan.persons_on_board and
            self.emergency_equipment_data_id == flight_plan.emergency_equipment_data_id and
            self.emergency_equipment_data == flight_plan.emergency_equipment_data and
            self.remarks == flight_plan.remarks and
            self.remarks_details == flight_plan.remarks_details and
            self.pilot_id == flight_plan.pilot_id and
            self.filled_by_user_id == flight_plan.filled_by_user_id and
            self.document_signature_filename == flight_plan.document_signature_filename
        )