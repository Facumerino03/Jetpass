import logging
from flask import Blueprint, request
from app.mapping import FlightPlanSchema
from app.services import FlightPlanServices
from app.utils import build_response
from app.validators import validate_with

flightplan_bp = Blueprint('flightplan', __name__)
flightplan_map = FlightPlanSchema()
flightplan_services = FlightPlanServices()

@flightplan_bp.route('/flightplans/<int:id>', methods=['GET'])
def get_flightplan(id: int):
    flightplan = flightplan_services.find(id)
    
    if flightplan is None:
        logging.info(f'FlightPlan not found id: {id}')
        return build_response('FlightPlan not found', code=404)
    
    logging.info(f'FlightPlan found id: {id}')
    return build_response('FlightPlan found', data=flightplan_map.dump(flightplan))

@flightplan_bp.route('/flightplans', methods=['GET'])
def get_all_flightplans():
    flightplans = flightplan_services.find_all()
    
    if not flightplans:
        logging.info('No flightplans found')
        return build_response('No flightplans found', code=404)
    
    logging.info('FlightPlans found')
    return build_response('FlightPlans found', data={'flightplans': flightplan_map.dump(flightplans, many=True)})

@flightplan_bp.route('/flightplans/create', methods=['POST'])
@validate_with(FlightPlanSchema)
def post_flightplan():
    flightplan_data = flightplan_map.load(request.json)
    flightplan_dict = flightplan_map.dump(flightplan_data)
    try:
        flightplan_saved = flightplan_services.save(flightplan_dict)
        logging.info(f'FlightPlan saved id: {flightplan_saved.id}')
        return build_response('FlightPlan saved', data=flightplan_map.dump(flightplan_saved), code=201)
    
    except ValueError as e:
        logging.error(f'Error saving flightplan: {e}')
        return build_response(str(e), code=400)

@flightplan_bp.route('/flightplans/<int:id>', methods=['PUT'])
@validate_with(FlightPlanSchema)
def update_flightplan(id: int):
    flightplan_data = flightplan_map.load(request.json)
    flightplan_dict = flightplan_map.dump(flightplan_data)
    
    existing_flightplan = flightplan_services.find(id)
    if existing_flightplan is None:
        logging.info(f'FlightPlan not found id: {id}')
        return build_response('FlightPlan not found', code=404)
    
    try:
        updated_flightplan = flightplan_services.update(flightplan_dict, id)
        logging.info(f'FlightPlan updated id: {id}')
        return build_response('FlightPlan updated', data=flightplan_map.dump(updated_flightplan))
    
    except ValueError as e:
        logging.error(f'Error updating flightplan: {e}')
        return build_response(str(e), code=400)

@flightplan_bp.route('/flightplans/<int:id>', methods=['DELETE'])
def delete_flightplan(id: int):
    flightplan = flightplan_services.find(id)
    
    if flightplan is None:
        logging.info(f'FlightPlan not found id: {id}')
        return build_response('FlightPlan not found', code=404)
    
    flightplan_services.delete(id)
    logging.info(f'FlightPlan deleted id: {id}')
    return build_response('FlightPlan deleted', code=200)