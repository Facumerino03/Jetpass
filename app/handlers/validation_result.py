from dataclasses import dataclass
from typing import Dict, List, Optional
from marshmallow import ValidationError

@dataclass
class ValidationResult:
    is_valid: bool
    errors: Dict[str, List[str]]
    
    @staticmethod
    def success() -> 'ValidationResult':
        """Crea un resultado de validación exitoso"""
        return ValidationResult(True, {})
    
    @staticmethod
    def failure(category: str, message: str) -> 'ValidationResult':
        """
        Crea un resultado de validación fallido
        
        Args:
            category: Categoría del error (ej: 'aerodrome', 'aircraft', etc)
            message: Mensaje descriptivo del error
        """
        return ValidationResult(False, {category: [message]})
    
    def add_error(self, category: str, message: str) -> None:
        """Agrega un error a una categoría específica"""
        self.is_valid = False
        if category not in self.errors:
            self.errors[category] = []
        self.errors[category].append(message)
    
    def merge(self, other: 'ValidationResult') -> 'ValidationResult':
        """
        Combina dos resultados de validación
        
        Args:
            other: Otro ValidationResult para combinar
        """
        if self.is_valid and other.is_valid:
            return ValidationResult.success()
        
        merged_errors = self.errors.copy()
        for category, messages in other.errors.items():
            if category not in merged_errors:
                merged_errors[category] = []
            merged_errors[category].extend(messages)
        
        return ValidationResult(False, merged_errors)
    
    def raise_if_invalid(self) -> None:
        """Lanza ValidationError si hay errores"""
        if not self.is_valid:
            # Convertir el diccionario de errores al formato esperado por marshmallow
            formatted_errors = {}
            for category, messages in self.errors.items():
                formatted_errors[category] = messages[0] if messages else ""
            
            raise ValidationError(message=formatted_errors)