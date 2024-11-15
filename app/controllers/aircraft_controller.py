import logging
from flask import Blueprint, request
from flask import Response
from app.mapping import AircraftSchema
from app.services import AircraftServices
from app.utils import build_response
from app.validators import validate_with

aircraft_bp = Blueprint('aircraft', __name__)
aircraft_map = AircraftSchema()
aircraft_services = AircraftServices()

@aircraft_bp.route('/aircraft/<int:id>', methods=['GET'])
def get_aircraft(id: int) -> Response:
    '''
    Get an aircraft by its id
    params:
        id: int
    returns:
        Response
    '''
    aircraft = aircraft_services.find(id)
    
    if aircraft is None:
        logging.info(f'Aircraft not found id: {id}')
        return build_response('Aircraft not found', code=404)
    
    logging.info(f'Aircraft found id: {id}')
    return build_response('Aircraft found', data=aircraft_map.dump(aircraft))

@aircraft_bp.route('/aircrafts', methods=['GET'])
def get_all_aircrafts() -> Response:
    '''
    Get all aircrafts
    returns:
        Response
    '''
    aircrafts = aircraft_services.find_all()
    
    if not aircrafts:
        logging.info('No aircrafts found')
        return build_response('No aircrafts found', code=404)
    
    logging.info('Aircrafts found')
    return build_response('Aircrafts found', data={'aircrafts': aircraft_map.dump(aircrafts, many=True)})

@aircraft_bp.route('/aircrafts/create', methods=['POST'])
@validate_with(AircraftSchema)
def post_aircraft() -> Response:
    '''
    Create an aircraft
    returns:
        Response
    '''
    aircraft = aircraft_map.load(request.json)
    try:
        aircraft_saved = aircraft_services.save(aircraft)
        logging.info(f'Aircraft saved id: {aircraft_saved.id}')
        return build_response('Aircraft saved', data=aircraft_map.dump(aircraft_saved), code=201)
    
    except ValueError as e:
        logging.error(f'Error saving aircraft: {e}')
        return build_response(str(e), code=400)

@aircraft_bp.route('/aircraft/<int:id>', methods=['PUT'])
@validate_with(AircraftSchema)
def update_aircraft(id: int) -> Response:
    '''
    Update an aircraft
    params:
        id: int
    returns:
        Response
    '''
    aircraft = aircraft_map.load(request.json)
    existing_aircraft = aircraft_services.find(id)
    
    if existing_aircraft is None:
        logging.info(f'Aircraft not found id: {id}')
        return build_response('Aircraft not found', code=404)
    
    try:
        updated_aircraft = aircraft_services.update(aircraft, id)
        logging.info(f'Aircraft updated id: {id}')
        return build_response('Aircraft updated', data=aircraft_map.dump(updated_aircraft))
    
    except ValueError as e:
        logging.error(f'Error updating aircraft: {e}')
        return build_response(str(e), code=400)

@aircraft_bp.route('/aircraft/<int:id>', methods=['DELETE'])
def delete_aircraft(id: int) -> Response:
    '''
    Delete an aircraft
    params:
        id: int
    returns:
        Response
    '''
    aircraft = aircraft_services.find(id)
    
    if aircraft is None:
        logging.info(f'Aircraft not found id: {id}')
        return build_response('Aircraft not found', code=404)
    
    aircraft_services.delete(id)
    logging.info(f'Aircraft deleted id: {id}')
    return build_response('Aircraft deleted', code=200)