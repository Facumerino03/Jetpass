from marshmallow import Schema, fields, post_load, validate
from app.models import Airport

class AirportSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    airport_code = fields.String(required=True, validate=validate.Length(max=4))
    city = fields.String(required=True)
    country = fields.String(required=True)
    south_coordinates = fields.Float(required=True)
    west_coordinates = fields.Float(required=True)
    latitude = fields.Float(required=True)
    elevation = fields.Float(required=True)
    runway_length = fields.Float(required=True)
    traffic_type_allowed = fields.String(required=True)

    @post_load
    def bind_airport(self, data, **kwargs):
        return Airport(**data)