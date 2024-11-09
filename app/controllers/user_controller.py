import logging
from flask import Blueprint, request
from app.mapping import UserSchema
from app.services import UserServices
from app.utils import build_response
from app.validators import validate_with

user_bp = Blueprint('user', __name__)
user_map = UserSchema()
user_services = UserServices()

@user_bp.route('/user/<int:id>', methods=['GET'])
def get_user(id: int):
    user = user_services.find(id)
    
    if user is None:
        logging.info(f'User not found id: {id}')
        return build_response('User not found', code=404)
    
    logging.info(f'User found id: {id}')
    return build_response('User found', data=user_map.dump(user))

@user_bp.route('/users', methods=['GET'])
def get_all_users():
    users = user_services.find_all()
    
    if not users:
        logging.info('No users found')
        return build_response('No users found', code=404)
    
    logging.info('Users found')
    return build_response('Users found', data={'users': user_map.dump(users, many=True)})

@user_bp.route('/users/create', methods=['POST'])
@validate_with(UserSchema)
def post_user():
    user = user_map.load(request.json)
    try:
        user_saved = user_services.save(user)
        logging.info(f'User saved id: {user_saved.id}')
        return build_response('User saved', data=user_map.dump(user_saved), code=201)
    except ValueError as e:
        logging.error(f'Error saving user: {e}')
        return build_response(str(e), code=400)

@user_bp.route('/user/<int:id>', methods=['PUT'])
@validate_with(UserSchema)
def update_user(id: int):
    user = user_map.load(request.json)
    
    existing_user = user_services.find(id)
    if existing_user is None:
        logging.info(f'User not found id: {id}')
        return build_response('User not found', code=404)
    
    try:
        updated_user = user_services.update(user, id)
        logging.info(f'User updated id: {id}')
        return build_response('User updated', data=user_map.dump(updated_user))
    
    except ValueError as e:
        logging.error(f'Error updating user: {e}')
        return build_response(str(e), code=400)

@user_bp.route('/user/<int:id>', methods=['DELETE'])
def delete_user(id:int):
    user = user_services.find(id)
    
    if user is None:
        logging.info(f'User not found id: {id}')
        return build_response('User not found', code=404)
    
    user_services.delete(id)
    logging.info(f'User deleted id: {id}')
    return build_response('User deleted', code=200)