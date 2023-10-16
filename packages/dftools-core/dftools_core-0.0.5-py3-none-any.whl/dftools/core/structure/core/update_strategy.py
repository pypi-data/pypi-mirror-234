from enum import auto
from strenum import StrEnum

class FieldUpdateStrategy(StrEnum):
    DATA_PROCESS = auto()
    ENGINEERING = auto()
    REPORTING = auto()
    BUSINESS = auto()
    
class UpdateStrategyCategory(StrEnum):
    GLOBAL = auto()
    NEW = auto()
    UPDATE = auto()
    DELETION = auto()