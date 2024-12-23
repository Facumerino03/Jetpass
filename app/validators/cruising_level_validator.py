from marshmallow import ValidationError # type: ignore
import re

def validate_cruising_level(value: str) -> ValidationError:
    '''
    Validates the cruising level format.
    It should be 'S' followed by four digits, 'A' followed by three digits, 'M' followed by four digits, or 'VFR'.
    
    param:
        value: str
    return:
        ValidationError
    '''
    pattern = re.compile(r'^(S\d{4}|A\d{3}|M\d{4}|VFR)$')
    if not pattern.match(value):
        raise ValidationError("Invalid cruising level format. It should be 'S' followed by four digits, 'A' followed by three digits, 'M' followed by four digits, or 'VFR'.")