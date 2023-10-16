import dataclasses
from dataclasses import dataclass
from collections.abc import Hashable

from dftools.core.structure.core.databank import DataBank
from dftools.utils import DfDataClassObj, DictDecoderInfo

@dataclass
class NamespaceImpl(DfDataClassObj):

    databank : DataBank
    catalog : str
    namespace : str
    
    def _get_dict_decoder_info() -> DictDecoderInfo:
        return DictDecoderInfo(["databank"], ["databank", "catalog", "namespace"], {"databank" : DataBank})
    
    @classmethod
    def _default_instance(cls):
        return cls(databank=DataBank._default_instance(), catalog='', namespace='')
    
@dataclass
class Namespace(DfDataClassObj, Hashable):

    databank_name : str
    catalog : str
    namespace : str
    
    def _get_dict_decoder_info() -> DictDecoderInfo:
        return DictDecoderInfo(["databank_name"], ["databank_name", "catalog", "namespace"])
    
    @classmethod
    def _default_instance(cls):
        return cls(databank_name='', catalog='', namespace='')
    
    def __hash__(self) -> int:
        return hash(repr(self))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return dataclasses.asdict(self) == dataclasses.asdict(other)
    