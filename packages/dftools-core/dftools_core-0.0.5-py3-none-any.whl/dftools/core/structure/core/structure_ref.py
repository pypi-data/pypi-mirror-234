from dataclasses import dataclass

from dftools.utils import DfJsonLoadable, DictDecoderInfo

@dataclass
class StructureRef(DfJsonLoadable):

    databank_name : str
    catalog : str
    namespace : str
    structure_name : str

    def _get_dict_decoder_info() -> DictDecoderInfo:
        return DictDecoderInfo(["databank_name", "catalog", "namespace", "structure_name"], ["databank_name", "catalog", "namespace", "structure_name"])
    
    @classmethod
    def _default_instance(cls):
        return cls(databank_name='', catalog='', namespace='', structure_name='')