import logging
from flask import Blueprint, request
from app.mapping import AirportSchema
from app.services import AirportServices
from app.utils import build_response
from app.validators import validate_with

airport_bp = Blueprint('airport', __name__)
airport_map = AirportSchema()
airport_services = AirportServices()

@airport_bp.route('/airport/<int:id>', methods=['GET'])
def get_airport(id: int):
    airport = airport_services.find(id)
    
    if airport is None:
        logging.info(f'Airport not found id: {id}')
        return build_response('Airport not found', code=404)
    
    logging.info(f'Airport found id: {id}')
    return build_response('Airport found', data=airport_map.dump(airport))

@airport_bp.route('/airports', methods=['GET'])
def get_all_airports():
    airports = airport_services.find_all()
    
    if not airports:
        logging.info('No airports found')
        return build_response('No airports found', code=404)
    
    logging.info('Airports found')
    return build_response('Airports found', data={'airports': airport_map.dump(airports, many=True)})

@airport_bp.route('/airports/create', methods=['POST'])
@validate_with(AirportSchema)
def post_airport():
    airport = airport_map.load(request.json)
    try:
        airport_saved = airport_services.save(airport)
        logging.info(f'Airport saved id: {airport_saved.id}')
        return build_response('Airport saved', data=airport_map.dump(airport_saved), code=201)
    except ValueError as e:
        logging.error(f'Error saving airport: {e}')
        return build_response(str(e), code=400)

@airport_bp.route('/airport/<int:id>', methods=['PUT'])
@validate_with(AirportSchema)
def update_airport(id: int):
    airport = airport_map.load(request.json)
    
    existing_airport = airport_services.find(id)
    if existing_airport is None:
        logging.info(f'Airport not found id: {id}')
        return build_response('Airport not found', code=404)
    
    try:
        updated_airport = airport_services.update(airport, id)
        logging.info(f'Airport updated id: {id}')
        return build_response('Airport updated', data=airport_map.dump(updated_airport))
    
    except ValueError as e:
        logging.error(f'Error updating airport: {e}')
        return build_response(str(e), code=400)

@airport_bp.route('/airport/<int:id>', methods=['DELETE'])
def delete_airport(id:int):
    airport = airport_services.find(id)
    
    if airport is None:
        logging.info(f'Airport not found id: {id}')
        return build_response('Airport not found', code=404)
    
    airport_services.delete(id)
    logging.info(f'Airport deleted id: {id}')
    return build_response('Airport deleted', code=200)