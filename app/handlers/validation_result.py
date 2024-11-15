from dataclasses import dataclass
from typing import Dict, List, Optional
from marshmallow import ValidationError # type: ignore

@dataclass
class ValidationResult:
    '''
    Represents the result of a validation process
    '''
    is_valid: bool
    errors: Dict[str, List[str]]
    
    @staticmethod
    def success() -> 'ValidationResult':
        '''
        Create a successful validation result
        returns:
            ValidationResult
        '''
        return ValidationResult(True, {})
    
    @staticmethod
    def failure(category: str, message: str) -> 'ValidationResult':
        '''
        Create a failed validation result
        params:
            category: Error category (e.g: 'aerodrome', 'aircraft', etc)
            message: Descriptive error message
        returns:
            ValidationResult
        '''
        return ValidationResult(False, {category: [message]})
    
    def add_error(self, category: str, message: str) -> None:
        '''
        Add an error to a specific category
        params:
            category: Error category (e.g: 'aerodrome', 'aircraft', etc)
            message: Descriptive error message
        '''
        self.is_valid = False
        if category not in self.errors:
            self.errors[category] = []
        self.errors[category].append(message)
    
    def merge(self, other: 'ValidationResult') -> 'ValidationResult':
        '''
        Merge two validation results
        params:
            other: Another ValidationResult to merge
        returns:
            ValidationResult
        '''
        if self.is_valid and other.is_valid:
            return ValidationResult.success()
        
        merged_errors = self.errors.copy()
        for category, messages in other.errors.items():
            if category not in merged_errors:
                merged_errors[category] = []
            merged_errors[category].extend(messages)
        
        return ValidationResult(False, merged_errors)
    
    def raise_if_invalid(self) -> None:
        '''
        Raise ValidationError if there are errors
        '''
        if not self.is_valid:
            formatted_errors = {}
            for category, messages in self.errors.items():
                formatted_errors[category] = messages[0] if messages else ""
            
            raise ValidationError(message=formatted_errors)