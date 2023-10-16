from dataclasses import dataclass, field
from typing import Dict, List

from dftools.utils import DfDataClassObj, DictDecoderInfo

@dataclass
class FieldNamingMapping(DfDataClassObj):
    """
        Example of field naming mapping dictionnary :
            {
                'prefix' : 'PREFIX_VALUE'
                , 'suffix' : 'SUFFIX_VALUE'
                , 'rules' :
                    {
                    'name' : {'override_name' : 'MGN_PDT_CAT_LV0'}
                    , 'sdesc1' : {'override_name' : 'MGN_PDT_CAT_LV0_SHT_FRE_DSC'}
                    , 'sdesc2' : {'override_name' : 'MGN_PDT_CAT_LV0_SHT_ENG_DSC'}
                    , 'ldesc1' : {'override_name' : 'MGN_PDT_CAT_LV0_LNG_FRE_DSC'}
                    , 'ldesc2' : {'override_name' : 'MGN_PDT_CAT_LV0_LNG_ENG_DSC'}
                    }
            }

        """
    
    prefix : str = ''
    suffix : str = ''
    rules : Dict[str, Dict[str, str]] = field(default_factory=dict)

    def _get_dict_decoder_info() -> DictDecoderInfo:
        return DictDecoderInfo([], ["prefix", "suffix", "rules"], {})

    @classmethod
    def _default_instance(cls):
        return cls(prefix='', suffix='', rules = {})
    
    def get_fields_mapped(self) -> List[str]:
        return list(self.rules.keys())

    def has_specific_naming_rule(self, name : str) -> bool:
        """
        Checks if the provided field name has a specific naming rule
        
        Parameters
        -----------
            name : the field name to check
        
        Returns
        -----------
            True if the field name has a specific naming rule, False otherwise
        """
        field_naming_rule = self.get_field_naming_rule(name)
        if field_naming_rule is None: 
            return False
        return 'rule' in field_naming_rule.keys()

    def get_field_naming_rule(self, name : str) -> Dict[str, str]:
        """
        Get the field naming rule for a specific field name
        
        Parameters
        -----------
            name : the field name
        
        Returns
        -----------
            The field naming rule for the provided field name (the target naming of the field)
        """
        if name in list(self.rules.keys()):
            return self.rules[name]
        return None

    def get_target_field_name(self, name : str) -> str:
        """
        Get the target field name for an input field name
        
        Parameters
        -----------
            name : the field name
        
        Returns
        -----------
            The target field name for this field naming rules
        """
        fld_specific_naming_rule = self.get_field_naming_rule(name)
        if fld_specific_naming_rule is None:
            return name
        if 'override_name' in fld_specific_naming_rule.keys():
            return fld_specific_naming_rule['override_name']
        rule = fld_specific_naming_rule['rule']
        rule_params = {
            "field_general_prefix" : self.prefix
            , "field_general_suffix" : self.suffix
            , "prefix" : fld_specific_naming_rule['prefix'] if 'prefix' in fld_specific_naming_rule.keys() else ''
            , "suffix" : fld_specific_naming_rule['suffix'] if 'suffix' in fld_specific_naming_rule.keys() else ''
        }
        return eval(rule, None, rule_params)