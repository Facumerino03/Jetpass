from marshmallow import Schema, fields, validate, post_load
from app.models import User

class MessageSchema(Schema):

    message:str = fields.String(required=True, dump_only=True)
    code:str = fields.String(required=True, dump_only=True)
    data:dict = fields.Dict(required=False, dump_only=True)