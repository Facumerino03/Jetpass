from enum import Enum

class TrafficTypeAllowedEnum(Enum):
    '''
    Traffic type allowed
    '''
    TRANSOCEANIC = "Transoceanic"
    TRANSCONTINENTAL = "Transcontinental"
    INTERNATIONAL = "International"
    NATIONAL = "National"
    LOCAL = "Local"
    MINOR_AIRFIELD = "Minor Airfield"
    MINIMUM_LOAD_AIRFIELD = "Minimum Load Airfield"
    SMALL_AIRPORT = "Small Airport"
    HELIPORT = "Heliport"