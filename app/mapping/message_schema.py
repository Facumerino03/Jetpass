from marshmallow import Schema, fields #type: ignore

class MessageSchema(Schema):
    '''
    Message schema for serialization
    '''
    message:str = fields.String(required=True, dump_only=True)
    code:str = fields.String(required=True, dump_only=True)
    data:dict = fields.Dict(required=False, dump_only=True)