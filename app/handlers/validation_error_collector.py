from marshmallow import ValidationError # type: ignore
from typing import Dict, List, Any

class ValidationErrorCollector:
    '''
    Collects validation errors and formats them all together into a consistent response with the API response format:
    
    {
        "message": "Error in the request data",
        "data": {"errors": {field: [error_message]}}
        "code": 400
    }
    '''
    def __init__(self):
        self.errors: Dict[str, List[str]] = {}
    
    def add_error(self, category: str, message: str) -> None:
        """
        Add an error to a specific category
        
        params:
            category: Error category (e.g: 'aerodrome', 'aircraft', etc)
            message: Descriptive error message
        """
        if category not in self.errors:
            self.errors[category] = []
        self.errors[category].append(message)
    
    def has_errors(self) -> bool:
        """
        Check if there are accumulated errors
        returns:
            bool
        """
        return bool(self.errors)
    
    def get_errors(self) -> Dict[str, List[str]]:
        """
        Return all accumulated errors
        returns:
            Dict[str, List[str]]
        """
        return self.errors
    
    def raise_if_errors(self) -> None:
        """
        Raise ValidationError if there are accumulated errors
        """
        if self.has_errors():
            raise ValidationError(messages=self.errors)