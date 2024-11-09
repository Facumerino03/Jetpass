from marshmallow import Schema, fields, validate, post_load #type: ignore
from app.models import Pilot

class PilotSchema(Schema):
    id = fields.Integer(dump_only=True)
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    license_number = fields.String(required=True)

    @post_load
    def bind_pilot(self, data, **kwargs):
        return Pilot(**data)