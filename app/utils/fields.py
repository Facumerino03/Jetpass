from marshmallow import fields, ValidationError #type: ignore

class EnumField(fields.Field):
    def __init__(self, enum_cls, *args, **kwargs):
        self.enum_cls = enum_cls
        super().__init__(*args, **kwargs)

    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        return value.name

    def _deserialize(self, value, attr, data, **kwargs):
        try:
            return self.enum_cls[value]
        except KeyError:
            valid_values = [e.name for e in self.enum_cls]
            raise ValidationError(
                f"Invalid value '{value}'. Must be one of: {', '.join(valid_values)}.")