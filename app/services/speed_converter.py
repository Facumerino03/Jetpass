from typing import Tuple

class SpeedConverter:
    @staticmethod
    def parse_speed(speed: str) -> Tuple[str, float]:
        """
        Parsea una velocidad en formato N#### o K####
        Retorna una tupla con (unidad, valor numérico)
        """
        if not speed or len(speed) != 5:
            raise ValueError("Formato de velocidad inválido")
            
        unit = speed[0].upper()
        if unit not in ['N', 'K']:
            raise ValueError(f"Unidad de velocidad no soportada: {unit}")
            
        try:
            # Extraer los dígitos y convertirlos a float
            digits = speed[1:]
            value = float(digits)
            return unit, value
        except ValueError:
            raise ValueError(f"Valor de velocidad inválido: {digits}")

    @staticmethod
    def convert_to_knots(speed: str) -> float:
        """Convierte cualquier formato de velocidad a nudos"""
        unit, value = SpeedConverter.parse_speed(speed)
        
        if unit == 'N':
            return value
        elif unit == 'K':
            return value * 0.539957  # Factor de conversión de km/h a nudos
        else:
            raise ValueError(f"Unidad de velocidad no soportada: {unit}")