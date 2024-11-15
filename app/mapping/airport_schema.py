from marshmallow import Schema, fields, post_load, validate #type: ignore
from app.models import Airport
from app.models.enums import TrafficTypeAllowedEnum
from app.utils import EnumField

class AirportSchema(Schema):
    '''
    Airport schema for validation and serialization
    '''
    id:int = fields.Integer(dump_only=True)
    name:str = fields.String(required=True)
    airport_code:str = fields.String(required=True, validate=validate.Length(max=4))
    city:str = fields.String(required=True)
    country:str = fields.String(required=True)
    south_coordinates:float = fields.Float(required=True)
    west_coordinates:float = fields.Float(required=True)
    latitude:float = fields.Float(required=True)
    elevation:float = fields.Float(required=True)
    runway_length:float = fields.Float(required=True)
    traffic_type_allowed:TrafficTypeAllowedEnum = EnumField(TrafficTypeAllowedEnum, required=True)

    @post_load
    def bind_airport(self, data: dict, **kwargs) -> Airport:
        '''
        Bind data to an Airport model
        params:
            data: Dict
        returns:
            Airport
        '''
        return Airport(**data)