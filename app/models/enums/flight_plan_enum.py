from enum import Enum

class FlightRulesEnum(Enum):
    '''
    Flight rules
    '''
    I = "I"
    V = "V"
    Y = "Y"
    Z = "Z"

class FlightTypeEnum(Enum):
    '''
    Flight type
    '''
    S = "S"
    N = "N"
    G = "G"
    M = "M"
    X = "X"