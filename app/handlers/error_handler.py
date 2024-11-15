from marshmallow import ValidationError
from app.utils import response_builder
from typing import Dict, Any, Optional

class ErrorHandler:
    @staticmethod
    def handle_validation_error(error: ValidationError) -> Dict[str, Any]:
        """
        Maneja los errores de validación y los formatea en una respuesta consistente
        """
        if isinstance(error.messages, dict):
            return response_builder.build_response(
                message="Error de validación",
                data={"errors": error.messages},
                code=400
            )
        else:
            return response_builder.build_response(
                message=str(error),
                data=None,
                code=400
            )