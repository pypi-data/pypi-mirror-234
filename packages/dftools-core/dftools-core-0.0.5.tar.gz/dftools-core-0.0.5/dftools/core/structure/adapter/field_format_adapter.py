from dataclasses import dataclass, field
from typing import List, Tuple
from dftools.utils import DictDecoderInfo, DfDataClassObj

@dataclass
class FieldFormatAdaptRule(DfDataClassObj) :
    """
        Field Format Adaptation rule

        This defines an adaptation rule for a field
    """
    allowed_data_types : List[str] = field(default_factory=list)
    allowed_characterisations : List[str] = field(default_factory=list)
    target_data_type : str = 'STRING'
    length_rule : str = '0'
    precision_rule : str = '0'

    def _get_dict_decoder_info() -> DictDecoderInfo:
        return DictDecoderInfo([], ["allowed_data_types", "allowed_characterisations", "target_data_type", "length_rule", "precision_rule"], {})

    @classmethod
    def _default_instance(cls):
        return cls(allowed_data_types = [], allowed_characterisations = [], target_data_type = 'STRING', length_rule = '0', precision_rule = '0')
    
    def _all_characterisations_allowed(self) -> bool:
        return len(self.allowed_characterisations) == 0

    def _is_rule_applicable(self, data_type : str, characterisations : List[str]) -> bool:
        if data_type is None:
            return False
        characterisations_lcl = characterisations if characterisations is not None else []
        if data_type in self.allowed_data_types :
            if self._all_characterisations_allowed():
                return True
            else:
                if any(char in self.allowed_characterisations for char in characterisations_lcl):
                    return True
        return False

    def get_adapted_field_format(self, data_type : str, length : int = None, precision : int = None):
        new_data_type = self.target_data_type
        new_length = int(self.length_rule.format(data_type = data_type, length = length, precision = precision))
        new_precision = int(self.precision_rule.format(data_type = data_type, length = length, precision = precision))
        return (new_data_type, new_length, new_precision)
    
@dataclass
class FieldFormatAdapter(DfDataClassObj) :

    rules : List[FieldFormatAdaptRule] = field(default_factory=list)
    default_format : Tuple[str, int, int] = ('STRING', 256, 0)
    default_keep_source_format : bool = True
    
    def _get_dict_decoder_info() -> DictDecoderInfo:
        return DictDecoderInfo([], ["rules", "default_format", "default_keep_source_format"]
            , {"rules" : FieldFormatAdaptRule})

    @classmethod
    def _default_instance(cls):
        return cls(rules = [], default_format = ('STRING', 256, 0), default_keep_source_format = True)

    def get_adapted_field_format(self, data_type : str, length : int = None, precision : int = None, characterisations : list = None) -> tuple:
        for rule in self.rules :
            if rule._is_rule_applicable(data_type=data_type, characterisations=characterisations) :
                return rule.get_adapted_field_format(data_type, length, precision)
        return self.default_format if (not self.default_keep_source_format) else (data_type, length, precision)
