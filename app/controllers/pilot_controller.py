import logging
from flask import Blueprint, request
from app.mapping import PilotSchema
from app.services import PilotServices
from app.utils import build_response
from app.validators import validate_with

pilot_bp = Blueprint('pilot', __name__)
pilot_map = PilotSchema()
pilot_services = PilotServices()

@pilot_bp.route('/pilot/<int:id>', methods=['GET'])
def get_pilot(id: int):
    pilot = pilot_services.find(id)
    
    if pilot is None:
        logging.info(f'Pilot not found id: {id}')
        return build_response('Pilot not found', code=404)
    
    logging.info(f'Pilot found id: {id}')
    return build_response('Pilot found', data=pilot_map.dump(pilot))

@pilot_bp.route('/pilots', methods=['GET'])
def get_all_pilots():
    pilots = pilot_services.find_all()
    
    if not pilots:
        logging.info('No pilots found')
        return build_response('No pilots found', code=404)
    
    logging.info('Pilots found')
    return build_response('Pilots found', data={'pilots': pilot_map.dump(pilots, many=True)})

@pilot_bp.route('/pilots/create', methods=['POST'])
@validate_with(PilotSchema)
def post_pilot():
    pilot = pilot_map.load(request.json)
    try:
        pilot_saved = pilot_services.save(pilot)
        logging.info(f'Pilot saved id: {pilot_saved.id}')
        return build_response('Pilot saved', data=pilot_map.dump(pilot_saved), code=201)
    except ValueError as e:
        logging.error(f'Error saving pilot: {e}')
        return build_response(str(e), code=400)

@pilot_bp.route('/pilot/<int:id>', methods=['PUT'])
@validate_with(PilotSchema)
def update_pilot(id: int):
    pilot = pilot_map.load(request.json)
    
    existing_pilot = pilot_services.find(id)
    if existing_pilot is None:
        logging.info(f'Pilot not found id: {id}')
        return build_response('Pilot not found', code=404)
    
    try:
        updated_pilot = pilot_services.update(pilot, id)
        logging.info(f'Pilot updated id: {id}')
        return build_response('Pilot updated', data=pilot_map.dump(updated_pilot))
    
    except ValueError as e:
        logging.error(f'Error updating pilot: {e}')
        return build_response(str(e), code=400)

@pilot_bp.route('/pilot/<int:id>', methods=['DELETE'])
def delete_pilot(id:int):
    pilot = pilot_services.find(id)
    
    if pilot is None:
        logging.info(f'Pilot not found id: {id}')
        return build_response('Pilot not found', code=404)
    
    pilot_services.delete(id)
    logging.info(f'Pilot deleted id: {id}')
    return build_response('Pilot deleted', code=200)