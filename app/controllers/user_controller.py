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
user_services = UserServices()

@user_bp.route('/user/<int:id>', methods=['GET'])
def get(id: int):
    user = user_services.find(id)
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
    users = user_services.find_all()
    message_schema = MessageSchema()
    message_builder = MessageBuilder()
    
    if not users:
        logging.info('No users found')
        message_filled = message_builder.add_message('No users found').build()
        return message_schema.dump(message_filled), 404
    
    logging.info('Users found')
    message_filled = message_builder.add_message('Users found').add_data({'users': user_map.dump(users, many=True)}).build()
    return message_schema.dump(message_filled), 200

#TODO: patron decorador
@user_bp.route('/users/create', methods=['POST'])
@validate_with(UserSchema)
def post():
    user = user_map.load(request.json)
    message_schema = MessageSchema()
    message_builder = MessageBuilder()
    try:
        user_saved = user_services.save(user)
        logging.info(f'User saved id: {user_saved.id}')
        message_filled = message_builder.add_message('User saved').add_data(user_map.dump(user_saved)).build()
        return message_schema.dump(message_filled), 201
    except ValueError as e:
        logging.error(f'Error saving user: {e}')
        message_filled = message_builder.add_message(str(e)).build()
        return message_schema.dump(message_filled), 400

#@use_kwarg(UserSchema)
@user_bp.route('/user/<int:id>', methods=['PUT'])
@validate_with(UserSchema)
def put(id: int):
    user = user_map.load(request.json)
    message_schema = MessageSchema()
    message_builder = MessageBuilder()
    
    existing_user = user_services.find(id)
    if existing_user is None:
        logging.info(f'User not found id: {id}')
        message_filled = message_builder.add_message('User not found').build()
        return message_schema.dump(message_filled), 404
    
    try:
        updated_user = user_services.update(user, id)
        logging.info(f'User updated id: {id}')
        message_filled = message_builder.add_message('User updated').add_data(user_map.dump(updated_user)).build()
        return message_schema.dump(message_filled), 200
    except ValueError as e:
        logging.error(f'Error updating user: {e}')
        message_filled = message_builder.add_message(str(e)).build()
        return message_schema.dump(message_filled), 400

@user_bp.route('/user/<int:id>', methods=['DELETE'])
def delete(id:int):
    user = user_services.find(id)
    message_schema = MessageSchema()
    message_builder = MessageBuilder()
    
    if user is None:
        logging.info(f'User not found id: {id}')
        message_filled = message_builder.add_message('User not found').build()
        return message_schema.dump(message_filled), 404
    
    user_services.delete(id)
    logging.info(f'User deleted id: {id}')
    message_filled = message_builder.add_message('User deleted').add_code(100).build()
    return message_schema.dump(message_filled), 200