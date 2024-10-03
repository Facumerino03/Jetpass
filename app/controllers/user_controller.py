from flask import Blueprint, jsonify
from app.mapping import UserMap
from app.services import UserServices


user_bp = Blueprint('user', __name__)
user_map = UserMap()

@user_bp.route('/users/<int:id>', methods=['GET'])
def get(id: int):
    user = UserServices.find(id)
    return user_map.dumps(user, many=False), 200

@user_bp.route('/users', methods=['GET'])
def get_all():
    users = UserServices.find_all()
    return user_map.dumps(users, many=True), 200

@user_bp.route('/users', methods=['POST'])
def post():
    pass

@user_bp.route('/users', methods=['PUT'])
def put():
    pass

@user_bp.route('/users', methods=['DELETE'])
def delete():
    pass