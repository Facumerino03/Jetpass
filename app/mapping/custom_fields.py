from marshmallow import fields, ValidationError #type: ignore
from app.models.enums import TrafficTypeAllowedEnum

class EnumField(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        return value.name

    def _deserialize(self, value, attr, data, **kwargs):
        try:
            return TrafficTypeAllowedEnum[value]
        except KeyError:
            valid_values = [e.name for e in TrafficTypeAllowedEnum]
            raise ValidationError(f"Invalid traffic type allowed '{value}'. Must be one of: {', '.join(valid_values)}.")