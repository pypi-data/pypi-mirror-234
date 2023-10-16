from dataclasses import dataclass
from typing import List
from strenum import StrEnum

from dftools.utils import DfDataClassObj, DictDecoderInfo
from dftools.core.structure.core import Field

class FieldTemplateRelativePosition(StrEnum):
    START = 'START'
    END = 'END'

@dataclass
class FieldTemplate(DfDataClassObj):
    """
        Field Template

        This template provides a standard field instance to be used in the creation of a structure
    """

    name : str
    field : Field
    override_existing_field_on_characterisation : str = None
    relative_position : str = FieldTemplateRelativePosition.END
    
    def _get_dict_decoder_info() -> DictDecoderInfo:
        return DictDecoderInfo(["name", "field"], ["name", "field", "override_existing_field_on_characterisation", "relative_position"]
            , {"field" : Field})

    @classmethod
    def _default_instance(cls):
        return cls(name='', field=Field._default_instance()
                    , override_existing_field_on_characterisation = None, relative_position=FieldTemplateRelativePosition.END)
    
    def get_field_instance(self) -> Field:
        """
        Get a field instance for this field template
        
        Returns
        -----------
            A new field based on this template
        """
        return Field.deep_copy(self.field)
    