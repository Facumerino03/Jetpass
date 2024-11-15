from datetime import time
from marshmallow import Schema, fields, post_load, validate #type: ignore
from app.models import Aircraft
from app.models.enums import WakeTurbulenceCategoryEnum
from app.utils import EnumField
from app.validators import validate_speed_format

class AircraftSchema(Schema):
    '''
    Aircraft schema for validation and serialization
    '''
    id:int = fields.Integer(dump_only=True)
    aircraft_identification:str = fields.String(required=True, validate=validate.Length(max=7))
    aircraft_type:str = fields.String(required=True, validate=validate.Length(max=4))
    wake_turbulence_category:WakeTurbulenceCategoryEnum = EnumField(WakeTurbulenceCategoryEnum, required=True)
    equipment:str = fields.String(required=True)
    endurance:time = fields.Time(required=True, format='%H:%M')
    passenger_capacity:str = fields.String(required=True, validate=validate.Length(max=4))
    crew_capacity:int = fields.Integer(required=True)
    max_speed:str = fields.String(required=True, validate=validate_speed_format)
    aircraft_colour_and_marking:str = fields.String(required=True)

    @post_load
    def bind_aircraft(self, data: dict, **kwargs) -> Aircraft:
        '''
        Bind data to an Aircraft model
        params:
            data: Dict
        returns:
            Aircraft
        '''
        return Aircraft(**data)