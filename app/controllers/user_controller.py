import logging
from flask import Blueprint, jsonify, request
from app.mapping import UserSchema
from app.models.user import User
from app.services import UserServices
from app.mapping import MessageSchema
from app.services import Message, MessageBuilder
from app.validators import validate_with

user_bp = Blueprint('user', __name__)
user_map = UserSchema()

@user_bp.route('/user/<int:id>', methods=['GET'])
def get(id: int):
    user = UserServices.find(id)
    message_schema = MessageSchema()
    message_builder = MessageBuilder()
    
    if user is None:
        logging.info(f'User not found id: {id}')
        message_filled = message_builder.add_message('User not found').build()
        return message_schema.dump(message_filled), 404
    
    logging.info(f'User found id: {id}')
    message_filled = message_builder.add_message('User found').add_data(user_map.dump(user)).build()
    return message_schema.dump(message_filled), 200

@user_bp.route('/users', methods=['GET'])
def get_all():
    logging.info('Users found')
    users = UserServices.find_all()
    message_schema = MessageSchema()
    message_builder = MessageBuilder()
    message_filled = message_builder.add_message('Users found').add_data({'users': user_map.dump(users, many=True)}).build()
    return message_schema.dump(message_filled), 200

#TODO: patron decorador
@user_bp.route('/users', methods=['POST'])
@validate_with(UserSchema)
def post():
    user = user_map.load(request.json)
    user_services = UserServices.save(user)
    logging.info(f'User saved id: {user.id}')
    message_schema = MessageSchema()
    message_builder = MessageBuilder()
    message_filled = message_builder.add_message('User saved').add_data(user_map.dump(user_services)).build()
    return message_schema.dump(message_filled), 201

#@use_kwarg(UserSchema)
@user_bp.route('/user/<int:id>', methods=['PUT'])
#@validate_with(UserSchema)
def put(id: int):
    user = user_map.load(request.json)
    
    if user is None:
        logging.info(f'User not found id: {id}')
        message_schema = MessageSchema()
        message_builder = MessageBuilder()
        message_filled = message_builder.add_message('User not found').build()
        return message_schema.dump(message_filled), 404
    
    updated_user = UserServices.update(user, id)
    logging.info(f'User updated id: {id}')
    message_schema = MessageSchema()
    message_builder = MessageBuilder()
    message_filled = message_builder.add_message('User updated').add_data(user_map.dump(updated_user)).build()
    
    return message_schema.dump(message_filled), 200
    

@user_bp.route('/user/<int:id>', methods=['DELETE'])
def delete(id:int):
    UserServices.delete(id)
    logging.info(f'User deleted id: {id}')
    
    message_schema = MessageSchema()
    message_builder = MessageBuilder()
    message_filled = message_builder.add_message('User deleted').add_code(100).build()
    return message_schema.dump(message_filled), 200