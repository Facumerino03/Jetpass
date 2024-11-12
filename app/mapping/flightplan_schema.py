from marshmallow import Schema, fields, post_load
from app.models import FlightPlan
from app.models.enums import FlightRulesEnum, FlightTypeEnum
from app.utils import EnumField
from app.mapping.emergency_equipment_data_schema import EmergencyEquipmentDataSchema

class FlightPlanSchema(Schema):
    id = fields.Integer(dump_only=True)
    submission_date = fields.DateTime(required=True)
    priority = fields.String(required=True)
    address_to = fields.String(required=True)
    filing_time = fields.DateTime(required=True)
    originator = fields.String(required=True)
    message_type = fields.String(required=True)
    aircraft_id = fields.Integer(required=True)
    flight_rules = EnumField(FlightRulesEnum, by_value=True, required=True)
    flight_type = EnumField(FlightTypeEnum, by_value=True, required=True)
    number_of_aircraft = fields.Integer(required=True)
    pilot_id = fields.Integer(required=True)
    departure_aerodrome_id = fields.Integer(required=True)
    departure_time = fields.DateTime(required=True)
    cruising_speed = fields.String(required=True)
    cruising_level = fields.String(required=True)
    route = fields.String(required=True)
    destination_aerodrome_id = fields.Integer(required=True)
    total_estimated_elapsed_time = fields.String(required=True)
    first_alternative_aerodrome_id = fields.Integer(required=True)
    second_alternative_aerodrome_id = fields.Integer(required=True)
    other_information = fields.String(required=True)
    persons_on_board = fields.Integer(required=True)
    emergency_equipment_data_id = fields.Integer(dump_only=True)
    remarks = fields.Boolean(required=True)
    remarks_details = fields.String(required=True)
    filled_by_user_id = fields.Integer(required=True)
    document_signature_filename = fields.String(required=True)
    emergency_equipment_data = fields.Nested(EmergencyEquipmentDataSchema, required=True)

    @post_load
    def make_flightplan(self, data, **kwargs):
        return FlightPlan(**data)