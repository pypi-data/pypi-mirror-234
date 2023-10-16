from dataclasses import dataclass
from typing import Optional

from dftools.utils import DfJsonLoadable, DictDecoderInfo

@dataclass
class DataBank(DfJsonLoadable):

    """ 
        A databank represents the standard access point to any object storage (database, cloud provider, Saas application, ...)
    """
    name : str
    version : Optional[str]
    sub_version : Optional[str]

    def _get_dict_decoder_info() -> DictDecoderInfo:
        return DictDecoderInfo(["name"], ["name", "version", "sub_version"], {})

    @classmethod
    def _default_instance(cls):
        return cls(name='', version='', sub_version='')