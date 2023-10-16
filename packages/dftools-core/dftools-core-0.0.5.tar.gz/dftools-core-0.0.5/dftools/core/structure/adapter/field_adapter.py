from dataclasses import dataclass, field
from typing import Dict, List
from dftools.utils import DictDecoderInfo, DfDataClassObj

from dftools.core.structure.adapter.field_format_adapter import FieldFormatAdapter
from dftools.core.structure.core import Field, FieldCharacterisation, FieldCharacterisationStd
    
@dataclass
class FieldAdapter(DfDataClassObj) :

    name_rule : str = 'original_field.name'
    desc_rule : str = 'original_field.desc'
    all_fields_optional : bool = False
    keep_tec_key : bool = True
    keep_func_key : bool = True
    orig_to_new_characterisation_mapping : Dict[str, str] = field(default_factory=dict)
    field_format_adapter : FieldFormatAdapter = None
    field_names_to_exclude : List[str] = field(default_factory=list)
    field_data_types_to_exclude : List[str] = field(default_factory=list)
    field_characterisations_to_exclude : List[str] = field(default_factory=list)
    exclude_fields_without_characterisations : bool = False
    
    def _get_dict_decoder_info() -> DictDecoderInfo:
        return DictDecoderInfo([]
            , ["name_rule", "desc_rule", "all_fields_optional", "keep_tec_key", "keep_func_key"
               , "orig_to_new_characterisation_mapping", "field_format_adapter", "field_names_to_exclude"
               , "field_data_types_to_exclude", "field_characterisations_to_exclude", "exclude_fields_without_characterisations"]
            , {"field_format_adapter" : FieldFormatAdapter})

    @classmethod
    def _default_instance(cls):
        return cls(name_rule = 'original_field.name', desc_rule = 'original_field.desc', all_fields_optional=False
            , keep_tec_key = True, keep_func_key = True, orig_to_new_characterisation_mapping = {}, field_format_adapter = None
            , field_names_to_exclude=[], field_data_types_to_exclude=[], field_characterisations_to_exclude=[]
            , exclude_fields_without_characterisations = False)

    def should_field_be_adapted(self, field : Field) -> bool:
        if (field.name not in self.field_names_to_exclude) \
            & (field.data_type not in self.field_data_types_to_exclude) \
            & (len([characterisation.name 
                    for characterisation in field.characterisations 
                    if characterisation.name in self.field_characterisations_to_exclude]) == 0 ) \
            & ( ( not self.exclude_fields_without_characterisations ) | (len(field.characterisations) > 0) ):
            return True
        return False
    
    def create_field(self
        , original_field : Field
        , override_params : Dict[str, str] = {}
        ) -> Field:
        """
        Creates a field based on this template
        
        Parameters
        -----------
            original_field : the original field
            override_params : the override parameters (allowed override parameters are "field_name")

        Returns
        -----------
            The new field
        """
        new_characterisations = []
        for characterisation in original_field.characterisations:
            if characterisation.name == FieldCharacterisationStd.MANDATORY:
                if not(self.all_fields_optional):
                    new_characterisations.append(FieldCharacterisation(FieldCharacterisationStd.MANDATORY, None))
            elif characterisation.name == FieldCharacterisationStd.TEC_ID:
                if self.keep_tec_key:
                    new_characterisations.append(FieldCharacterisation(FieldCharacterisationStd.TEC_ID, None))
            elif characterisation.name == FieldCharacterisationStd.FCT_ID:
                if self.keep_func_key:
                    new_characterisations.append(FieldCharacterisation(FieldCharacterisationStd.FCT_ID, None))
            elif characterisation.name in list(self.orig_to_new_characterisation_mapping.keys()):
                tgt_characterisation_name = self.orig_to_new_characterisation_mapping[characterisation.name]
                new_characterisations.append(FieldCharacterisation(tgt_characterisation_name, None))
            else:
                new_characterisations.append(characterisation)
        
        new_field_format = self.field_format_adapter.get_adapted_field_format(data_type=original_field.data_type
            , length=original_field.length, precision=original_field.precision
            , characterisations=original_field.characterisations) \
            if self.field_format_adapter is not None else (original_field.data_type, original_field.length, original_field.precision)

        creation_param_dict = {}
        creation_param_dict['original_field'] = original_field
        creation_param_dict['override_params'] = override_params if override_params is not None else {}

        return Field(
            name = eval(self.name_rule, None, creation_param_dict)
            , desc = eval(self.desc_rule, None, creation_param_dict)
            , position = 0
            , data_type = new_field_format[0]
            , length = new_field_format[1]
            , precision = new_field_format[2]
            , default_value=original_field.default_value
            , characterisations=new_characterisations
            , sourcing_info=None
        )