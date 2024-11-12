from marshmallow import Schema, fields, post_load
from app.models import EmergencyEquipmentData

class EmergencyEquipmentDataSchema(Schema):
    id = fields.Integer(dump_only=True)
    radio_uhf = fields.Boolean(required=True)
    radio_vhf = fields.Boolean(required=True)
    radio_elt = fields.Boolean(required=True)
    survival_equipment = fields.Boolean(required=True)
    survival_polar = fields.Boolean(required=True)
    survival_desert = fields.Boolean(required=True)
    survival_maritime = fields.Boolean(required=True)
    survival_jungle = fields.Boolean(required=True)
    jackets = fields.Boolean(required=True)
    jackets_lights = fields.Boolean(required=True)
    jackets_fluorescein = fields.Boolean(required=True)
    jackets_radio_uhf = fields.Boolean(required=True)
    jackets_radio_vhf = fields.Boolean(required=True)
    dinghies = fields.Boolean(required=True)
    dinghies_number = fields.Integer(required=True)
    dinghies_capacity = fields.Integer(required=True)
    dinghies_cover = fields.Boolean(required=True)
    dinghies_cover_colour = fields.String(required=True)

    @post_load
    def make_emergency_equipment_data(self, data, **kwargs):
        return EmergencyEquipmentData(**data)