from marshmallow import ValidationError
from datetime import time
import re

def validate_utc_time(value: str) -> time:
    '''
    Validates the UTC time format.
    It should be in UTC format HHMM.
    '''
    pattern = re.compile(r'^[0-2][0-9][0-5][0-9]$')
    if not pattern.match(value):
        raise ValidationError("Invalid time format. It should be in UTC format HHMM.")
    
    try:
        hours = int(value[:2])
        minutes = int(value[2:])
        
        if hours > 23 or minutes > 59:
            raise ValidationError("Invalid time value. Hours should be between 00 and 23, and minutes between 00 and 59.")
        
        return time(hour=hours, minute=minutes)
    except ValueError:
        raise ValidationError("Invalid time format")