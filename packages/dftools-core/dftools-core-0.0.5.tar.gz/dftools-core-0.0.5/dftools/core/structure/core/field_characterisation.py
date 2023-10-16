from enum import auto
from dataclasses import dataclass
from typing import Optional, Dict
from dftools.utils import DfJsonLoadable, DictDecoderInfo
from strenum import StrEnum

class FieldConstraintType(StrEnum):
    NOT_ENFORCED='NotEnforced', 
    ENFORCED='Enforced'


class FieldCharacterisationTypeStd(StrEnum):
    IDENTIFICATION = auto()
    TECHNICAL = auto()
    DATA = auto()
    USAGE = auto()

class FieldCharacterisationSubTypeStd(StrEnum):
    ENTRY_IDENTIFICATION = auto()
    TEC_RECORD_INFO_SRC = auto()
    TEC_RECORD_INFO = auto()
    TEC_INGEST_INFO = auto()
    DATA_ENTRY = auto()

@dataclass
class FieldCharacterisation(DfJsonLoadable):
    name : str
    attributes : Optional[Dict[str, str]]
    
    def _get_dict_decoder_info() -> DictDecoderInfo:
        return DictDecoderInfo(["name"], ["name", "attributes"], {})

    @classmethod
    def _default_instance(cls):
        return cls(name=None, attributes={})
    

class FieldCharacterisationStd(StrEnum):
    TEC_ID = auto()
    FCT_ID = auto()
    UNIQUE = auto()
    MANDATORY = auto()

