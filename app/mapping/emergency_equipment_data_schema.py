from marshmallow import Schema, fields, post_load # type: ignore
from app.models import EmergencyEquipmentData

class EmergencyEquipmentDataSchema(Schema):
    '''
    EmergencyEquipmentData schema for validation and serialization
    '''
    id:int = fields.Integer(dump_only=True)
    radio_uhf:bool = fields.Boolean(required=True)
    radio_vhf:bool = fields.Boolean(required=True)
    radio_elt:bool = fields.Boolean(required=True)
    survival_equipment:bool = fields.Boolean(required=True)
    survival_polar:bool = fields.Boolean(required=True)
    survival_desert:bool = fields.Boolean(required=True)
    survival_maritime:bool = fields.Boolean(required=True)
    survival_jungle:bool = fields.Boolean(required=True)
    jackets:bool = fields.Boolean(required=True)
    jackets_lights:bool = fields.Boolean(required=True)
    jackets_fluorescein:bool = fields.Boolean(required=True)
    jackets_radio_uhf:bool = fields.Boolean(required=True)
    jackets_radio_vhf:bool = fields.Boolean(required=True)
    dinghies:bool = fields.Boolean(required=True)
    dinghies_number:int = fields.Integer(required=True)
    dinghies_capacity:int = fields.Integer(required=True)
    dinghies_cover:bool = fields.Boolean(required=True)
    dinghies_cover_colour:str = fields.String(required=True)

    @post_load
    def make_emergency_equipment_data(self, data: dict, **kwargs) -> EmergencyEquipmentData:
        '''
        Bind data to an EmergencyEquipmentData model
        params:
            data: Dict
        returns:
            EmergencyEquipmentData
        '''
        return EmergencyEquipmentData(**data)