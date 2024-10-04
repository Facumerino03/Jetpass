from email import message
from flask import Blueprint, jsonify
from app.mapping import UserSchema
from app.services import UserServices
from app.mapping import MessageSchema
from app.services import Message, MessageBuilder

user_bp = Blueprint('user', __name__)
user_map = UserSchema()

@user_bp.route('/user/<int:id>', methods=['GET'])
def get(id: int):
    user = UserServices.find(id)
    message_schema = MessageSchema()
    message_builder = MessageBuilder()
    message_filled = message_builder.add_message('User found').add_data(user_map.dump(user)).build()
    return message_schema.dump(message_filled), 200

@user_bp.route('/users', methods=['GET'])
def get_all():
    users = UserServices.find_all()
    message_schema = MessageSchema()
    message_builder = MessageBuilder()
    message_filled = message_builder.add_message('Users found').add_data(user_map.dump(users, many=True)).build()
    return message_schema.dump(message_filled), 200

@user_bp.route('/users', methods=['POST'])
def post():
    pass

@user_bp.route('/users', methods=['PUT'])
def put():
    pass

@user_bp.route('/users', methods=['DELETE'])
def delete():
    pass