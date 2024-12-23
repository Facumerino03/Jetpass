from marshmallow import Schema, fields, post_load #type: ignore
from app.models import Pilot

class PilotSchema(Schema):
    '''
    Pilot schema for validation and serialization
    '''
    id:int = fields.Integer(dump_only=True)
    first_name:str = fields.String(required=True)
    last_name:str = fields.String(required=True)
    license_number:str = fields.String(required=True)

    @post_load
    def bind_pilot(self, data: dict, **kwargs) -> Pilot:
        '''
        Bind data to an Pilot model
        params:
            data: Dict
        returns:
            Pilot
        '''
        return Pilot(**data)