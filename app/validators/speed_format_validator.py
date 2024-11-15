from marshmallow import ValidationError
import re

def validate_speed_format(value: str) -> None:
    '''
    Validates the speed format.
    It should be N (knots) or K (kilometers) followed by four digits.
    '''
    pattern = re.compile(r'^[NK]\d{4}$')
    if not pattern.match(value):
        raise ValidationError("Invalid speed format. It should be N or K followed by four digits.")