from marshmallow import ValidationError # type: ignore
from app.utils import response_builder
from flask import Response

class ErrorHandler:
    @staticmethod
    def handle_validation_error(error: ValidationError) -> Response:
        """
        Handle marshmallow validation errors formatting them into a consistent response with the API response format:
        
        {
            "message": "Error in the request data",
            "data": {"errors": {field: [error_message]}}
            "code": 400
        }
        
        params:
            error: ValidationError
        returns:
            Response
        """
        if isinstance(error.messages, dict):
            return response_builder.build_response(
                message="Validation error",
                data={"errors": error.messages},
                code=400
            )
        else:
            return response_builder.build_response(
                message=str(error),
                data=None,
                code=400
            )