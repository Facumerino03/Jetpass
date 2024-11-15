from marshmallow import ValidationError
from typing import Dict, List, Any

class ValidationErrorCollector:
    def __init__(self):
        self.errors: Dict[str, List[str]] = {}
    
    def add_error(self, category: str, message: str) -> None:
        """
        Agrega un error a una categoría específica
        
        Args:
            category: Categoría del error (ej: 'aerodrome', 'aircraft', etc)
            message: Mensaje descriptivo del error
        """
        if category not in self.errors:
            self.errors[category] = []
        self.errors[category].append(message)
    
    def has_errors(self) -> bool:
        """Verifica si hay errores acumulados"""
        return bool(self.errors)
    
    def get_errors(self) -> Dict[str, List[str]]:
        """Retorna todos los errores acumulados"""
        return self.errors
    
    def raise_if_errors(self) -> None:
        """Lanza ValidationError si hay errores acumulados"""
        if self.has_errors():
            raise ValidationError(messages=self.errors)