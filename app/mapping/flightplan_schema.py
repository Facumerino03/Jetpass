from datetime import date, datetime, time
from marshmallow import Schema, fields, post_load # type: ignore
from app.models import FlightPlan
from app.models.enums import FlightRulesEnum, FlightTypeEnum
from app.utils import EnumField
from app.mapping.emergency_equipment_data_schema import EmergencyEquipmentDataSchema
from app.validators import validate_speed_format, validate_cruising_level, validate_utc_time

class FlightPlanSchema(Schema):
    '''
    FlightPlan schema for validation and serialization
    '''
    id:int = fields.Integer(dump_only=True)
    submission_date:datetime = fields.DateTime(dump_only=True)
    priority:str = fields.String(required=True)
    address_to:str = fields.String(required=True)
    filing_time:str = fields.String(required=True, validate=validate_utc_time)
    originator:str = fields.String(required=True)
    message_type:str = fields.String(required=True)
    aircraft_id:int = fields.Integer(required=True)
    flight_rules:FlightRulesEnum = EnumField(FlightRulesEnum, by_value=True, required=True)
    flight_type:FlightTypeEnum = EnumField(FlightTypeEnum, by_value=True, required=True)
    number_of_aircraft:int = fields.Integer(required=True)
    pilot_id:int = fields.Integer(required=True)
    departure_aerodrome_id:int = fields.Integer(required=True)
    departure_date:date = fields.Date(required=True, format='%Y-%m-%d')
    departure_time:str = fields.String(required=True, validate=validate_utc_time)
    cruising_speed:str = fields.String(required=True, validate=validate_speed_format)
    cruising_level:str = fields.String(required=True, validate=validate_cruising_level)
    route:str = fields.String(required=True)
    destination_aerodrome_id:int = fields.Integer(required=True)
    total_estimated_elapsed_time:time = fields.Time(required=True, format='%H:%M')
    first_alternative_aerodrome_id:int = fields.Integer(required=True)
    second_alternative_aerodrome_id:int = fields.Integer(required=True)
    other_information:str = fields.String(required=True)
    persons_on_board:int = fields.Integer(required=True)
    emergency_equipment_data_id:int = fields.Integer(dump_only=True)
    remarks:bool = fields.Boolean(required=True)
    remarks_details:str = fields.String(required=True)
    filled_by_user_id:int = fields.Integer(required=True)
    document_signature_filename:str = fields.String(required=True)
    emergency_equipment_data:EmergencyEquipmentDataSchema = fields.Nested(EmergencyEquipmentDataSchema, required=True)

    @post_load
    def make_flightplan(self, data: dict, **kwargs) -> FlightPlan:
        '''
        Bind data to an FlightPlan model
        params:
            data: Dict
        returns:
            FlightPlan
        '''
        return FlightPlan(**data)