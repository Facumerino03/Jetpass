import logging
from flask import Blueprint, request, Response
from app.mapping import FlightPlanSchema
from app.services import FlightPlanServices, FlightPlanFormatterService
from app.utils import build_response
from app.validators import validate_with
from app.handlers import ErrorHandler
from marshmallow import ValidationError # type: ignore

flightplan_bp = Blueprint('flightplan', __name__)
flightplan_map = FlightPlanSchema()
flightplan_services = FlightPlanServices()

@flightplan_bp.route('/flightplans/<int:id>', methods=['GET'])
def get_flightplan(id: int) -> Response:
    '''
    Get a flightplan by its id
    params:
        id: int
    returns:
        Response
    '''
    flightplan = flightplan_services.find(id)
    
    if flightplan is None:
        logging.info(f'FlightPlan not found id: {id}')
        return build_response('FlightPlan not found', code=404)
    
    flightplan_data = flightplan_map.dump(flightplan)
    formatted_flightplan = FlightPlanFormatterService.format_for_response(flightplan_data)
    
    logging.info(f'FlightPlan found id: {id}')
    return build_response('FlightPlan found', data=formatted_flightplan)

@flightplan_bp.route('/flightplans', methods=['GET'])
def get_all_flightplans() -> Response:
    '''
    Get all flightplans
    returns:
        Response
    '''
    flightplans = flightplan_services.find_all()
    
    if not flightplans:
        logging.info('No flightplans found')
        return build_response('No flightplans found', code=404)
    
    flightplan_data = flightplan_map.dump(flightplans, many=True)
    formatted_flightplans = [FlightPlanFormatterService.format_for_response(flightplan) for flightplan in flightplan_data]
    
    logging.info('FlightPlans found')
    return build_response('FlightPlans found', data={'flightplans': formatted_flightplans})

@flightplan_bp.route('/flightplans/create', methods=['POST'])
@validate_with(FlightPlanSchema)
def post_flightplan() -> Response:
    '''
    Create a flightplan
    returns:
        Response
    '''
    flightplan_data = flightplan_map.load(request.json)
    flightplan_dict = flightplan_map.dump(flightplan_data)
    
    try:
        flightplan_saved = flightplan_services.save(flightplan_dict)
        logging.info(f'FlightPlan saved id: {flightplan_saved.id}')
        return build_response('FlightPlan saved', data=flightplan_map.dump(flightplan_saved), code=201)
    
    except ValidationError as e:
        return ErrorHandler.handle_validation_error(e)
    
    except ValueError as e:
        logging.error(f'Error saving flightplan: {e}')
        return build_response(str(e), code=400)

@flightplan_bp.route('/flightplans/<int:id>', methods=['DELETE'])
def delete_flightplan(id: int) -> Response:
    '''
    Delete a flightplan
    params:
        id: int
    returns:
        Response
    '''
    flightplan = flightplan_services.find(id)
    
    if flightplan is None:
        logging.info(f'FlightPlan not found id: {id}')
        return build_response('FlightPlan not found', code=404)
    
    flightplan_services.delete(id)
    logging.info(f'FlightPlan deleted id: {id}')
    return build_response('FlightPlan deleted', code=200)