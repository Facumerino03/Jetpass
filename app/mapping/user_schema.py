from marshmallow import Schema, fields, validate, post_load #type: ignore
from app.models import User

class UserSchema(Schema):
    '''
    User schema for validation and serialization
    '''
    id:int = fields.Integer(dump_only=True)
    firstname:str = fields.String(required=True)
    lastname:str = fields.String(required=True)
    dni:str = fields.String(required=True)
    email:str = fields.String(required=True, validate=validate.Email())
    phone:str = fields.String(required=True)
    address:str = fields.String(required=True)
    state:str = fields.String(required=True)
    city:str = fields.String(required=True)
    zipcode:str = fields.String(required=True)
    password:str = fields.String(load_only=True)
    
    @post_load
    def bind_user(self, data: dict, **kwargs) -> User:
        '''
        Bind data to an User model
        params:
            data: Dict
        returns:
            User
        '''
        return User(**data)