from flask import jsonify, request
from functools import wraps
from marshmallow import ValidationError #type: ignore

def validate_with(schema):
    '''
    Validates the request body with the given schema
    param:
        schema: Schema
    return:
        decorator
    '''
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                data = schema().load(request.json)
            except ValidationError as err:
                return jsonify(err.messages), 400
            return f(*args, **kwargs)
        return decorated_function
    return decorator