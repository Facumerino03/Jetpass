from typing import Tuple

class SpeedConverter:
    '''
    Class that handles the speed conversion
    '''
    
    @staticmethod
    def parse_speed(speed: str) -> Tuple[str, float]:
        '''
        Parses a speed in the format N#### or K####
        Returns a tuple with (unit, numeric value)
        
        param:
            speed: str
        return:
            Tuple[str, float]
        '''
        if not speed or len(speed) != 5:
            raise ValueError("Invalid speed format")
            
        unit = speed[0].upper()
        if unit not in ['N', 'K']:
            raise ValueError(f"Unidad de velocidad no soportada: {unit}")
            
        try:
            digits = speed[1:]
            value = float(digits)
            return unit, value
        except ValueError:
            raise ValueError(f"Valor de velocidad inválido: {digits}")

    @staticmethod
    def convert_to_knots(speed: str) -> float:
        '''
        Converts any speed format to knots
        
        param:
            speed: str
        return:
            float
        '''
        unit, value = SpeedConverter.parse_speed(speed)
        
        if unit == 'N':
            return value
        elif unit == 'K':
            return value * 0.539957  # Factor de conversión de km/h a nudos
        else:
            raise ValueError(f"Unidad de velocidad no soportada: {unit}")