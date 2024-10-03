from http import client
from flask import Blueprint, jsonify

home_bp = Blueprint('home', __name__)

@home_bp.route('/', methods=['GET'])
def get():
    return jsonify({'message': 'Hello World'}), 200
