from flask import Blueprint, jsonify
from app.mapping import MessageSchema
from app.services import Message, MessageBuilder
from flask import Response
from app.utils import build_response
import logging

home_bp = Blueprint('home', __name__)

@home_bp.route('/', methods=['GET'])
def get_home() -> Response:
    '''
    API Home - Documentation and available endpoints for flight plans management
    returns:
        Response
    '''
    api_docs = {
        'name': 'Jetpass API',
        'version': '1.0.0',
        'description': 'API for flight plans management',
        'endpoints': {
            'flightplans': {
                'GET /flightplans': 'Get all flight plans',
                'GET /flightplans/<id>': 'Get specific flight plan',
                'POST /flightplans/create': 'Create new flight plan',
                'DELETE /flightplans/<id>': 'Delete flight plan'
            },
            'aircraft': {
                'GET /aircraft/<id>': 'Get specific aircraft',
                'GET /aircrafts': 'Get all aircraft',
                'POST /aircrafts/create': 'Create new aircraft',
                'PUT /aircraft/<id>': 'Update aircraft',
                'DELETE /aircraft/<id>': 'Delete aircraft'
            },
            'pilots': {
                'GET /pilot/<id>': 'Get specific pilot',
                'GET /pilots': 'Get all pilots',
                'POST /pilots/create': 'Create new pilot',
                'PUT /pilot/<id>': 'Update pilot'
            },
            'airports': {
                'GET /airport/<id>': 'Get specific airport',
                'GET /airports': 'Get all airports',
                'POST /airports/create': 'Create new airport',
                'PUT /airport/<id>': 'Update airport'
            },
            'users': {
                'GET /user/<id>': 'Get specific user',
                'GET /users': 'Get all users'
            }
        },
        'api_version': '/api/v1',
        'documentation': 'For more details, check the complete documentation at /docs',
        'status': {
            'code': 200,
            'message': 'API is running correctly'
        }
    }
    
    logging.info('Home endpoint accessed')
    return build_response('Welcome to Jetpass API', data=api_docs)


