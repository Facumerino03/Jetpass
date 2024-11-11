from marshmallow import Schema, fields, post_load, validate #type: ignore
from app.models import Aircraft
from app.models.enums import WakeTurbulenceCategoryEnum
from app.utils import EnumField
from app.validators import validate_speed_format

class AircraftSchema(Schema):
    id = fields.Integer(dump_only=True)
    aircraft_identification = fields.String(required=True, validate=validate.Length(max=7))
    aircraft_type = fields.String(required=True, validate=validate.Length(max=4))
    wake_turbulence_category = EnumField(WakeTurbulenceCategoryEnum, required=True)
    equipment = fields.String(required=True)
    endurance = fields.Time(required=True, format='%H:%M')
    passenger_capacity = fields.String(required=True, validate=validate.Length(max=4))
    crew_capacity = fields.Integer(required=True)
    max_speed = fields.String(required=True, validate=validate_speed_format)
    aircraft_colour_and_marking = fields.String(required=True)

    @post_load
    def bind_aircraft(self, data, **kwargs):
        return Aircraft(**data)