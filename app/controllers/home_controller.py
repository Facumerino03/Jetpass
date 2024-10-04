from flask import Blueprint, jsonify
from app.mapping import MessageSchema
from app.services import Message, MessageBuilder

home_bp = Blueprint('home', __name__)

@home_bp.route('/', methods=['GET'])
def get():
    message_schema = MessageSchema()
    message_builder = MessageBuilder()
    message_filled = message_builder.add_message('Hello World').add_message('OK')
    return message_schema.dump(message_filled), 200


