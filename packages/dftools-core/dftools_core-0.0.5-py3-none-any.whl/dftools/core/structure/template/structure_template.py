import logging
from dataclasses import dataclass, field
from typing import List, Dict

from dftools.events import log_event
from dftools.events.events import CreatedStructureFromTemplate

from dftools.utils import DfDataClassObj, DictDecoderInfo
from dftools.core.structure.core import (
    Field, 
    Structure
)
from dftools.core.structure.adapter import FieldAdapter
from dftools.core.structure.template.field_template import FieldTemplate, FieldTemplateRelativePosition
from dftools.core.structure.template.field_naming_mapping import FieldNamingMapping

@dataclass
class StructureTemplate(DfDataClassObj):
    """
        Structure Template

        This template provides a standard way to create new structure based on a template and an original structure.
        List of parameters allowed for creation of structure based on template are : 
        - original_structure : Structure object
        ... (To be filled) !!!!!!!!

    """
    name : str
    name_rule : str = 'original_structure.name'
    desc_rule : str = 'original_structure.desc'
    type_rule : str = None
    mandatory_parameters : List[str] = field(default_factory=list)
    field_adapter : FieldAdapter = None
    field_templates : List[FieldTemplate] = field(default_factory=list)
    exclude_fields_wo_naming_mapping : bool = False

    def _get_dict_decoder_info() -> DictDecoderInfo:
        return DictDecoderInfo(["name", "field_adapter"]
            , ["name", "name_rule", "desc_rule", "type_rule", "mandatory_parameters", "field_adapter", "field_templates", "exclude_fields_wo_naming_mapping"]
            , {"field_adapter" : FieldAdapter, "field_templates" : FieldTemplate})

    @classmethod
    def _default_instance(cls):
        return cls(name='', name_rule='original_structure.name', desc_rule = 'original_structure.desc', type_rule=None
                   , mandatory_parameters = [], field_adapter = None, field_templates = [], exclude_fields_wo_naming_mapping = False)

    def __post_init__(self):
        self.logger = logging.getLogger(__name__)
    
    def create_structure(self, **kwargs) -> Structure:
        """
        Creates a structure based on this template
        
        Parameters
        -----------
            original_structure : the original structure
            field_naming_mapping : the field naming mapping (when standard mappings to apply)
            field_catalog : a dictionnary of all the standard fields known, if a field is to be generated 
                with a target field name available in this catalog, the field definition from the catalog
                should be used to create the new field

        Returns
        -----------
            The new structure
        """
        for parameter_name in self.mandatory_parameters:
            if parameter_name not in kwargs.keys():
                raise ValueError('Parameter ' + parameter_name + ' is mandatory for creating structure with template : ' + self.name)
        
        original_structure : Structure = kwargs['original_structure'] if 'original_structure' in kwargs.keys() else None
        field_naming_mapping : FieldNamingMapping = kwargs['field_naming_mapping'] if 'field_naming_mapping' in kwargs.keys() else FieldNamingMapping()
        field_catalog : Dict[str, Field] = kwargs['field_catalog'] if 'field_catalog' in kwargs.keys() else {}
        
        creation_param_dict = {}
        creation_param_dict['original_structure'] = original_structure
        
        new_structure = Structure(
            name = eval(self.name_rule, None, creation_param_dict)
            , desc = eval(self.desc_rule, None, creation_param_dict)
            , type = eval(self.type_rule, None, creation_param_dict)
            , row_count = 0
            , options = {}
            , content_type = {}
            , fields = []
            , sourcing_info = None
        )
        
        for field in original_structure.fields:
            if self.field_adapter.should_field_be_adapted(field):
                if ( not self.exclude_fields_wo_naming_mapping ) | ( field.name in field_naming_mapping.get_fields_mapped() ) :
                    if field_naming_mapping.has_specific_naming_rule(field.name):
                        # Whenever a specific naming rule is provided, this rules is of higher priority
                        new_structure.add_field(self.field_adapter.create_field(field
                            , override_params={"field_name" : field_naming_mapping.get_target_field_name(field.name)}))
                    else:
                        field_name_override = field_naming_mapping.get_target_field_name(field.name)
                        if field_name_override in field_catalog.keys():
                            # This means the field has a default definition to be considered
                            new_structure.add_field(self.field_adapter.create_field(field_catalog[field_name_override]))
                        else :
                            new_structure.add_field(self.field_adapter.create_field(field
                                , override_params={"field_name" : field_naming_mapping.get_target_field_name(field.name)}))
        
        self._update_structure_from_template_fields(new_structure)

        log_event(self.logger, CreatedStructureFromTemplate(structure_name = new_structure.name, template_name = self.name, original_structure_name = original_structure.name))
        return new_structure

    # Field Template methods
    def get_field_templates_with_existing_override_on_characterisation(self) -> List[FieldTemplate]:
        return [field_template for field_template in self.field_templates 
                if field_template.override_existing_field_on_characterisation is not None]
    
    def get_field_templates_at_start(self) -> List[FieldTemplate]:
        return [field_rule for field_rule in self.field_templates 
                if field_rule.relative_position == FieldTemplateRelativePosition.START]
    
    def get_field_templates_at_end(self) -> List[FieldTemplate]:
        return [field_rule for field_rule in self.field_templates 
                if field_rule.relative_position == FieldTemplateRelativePosition.END]
    
    def _update_structure_from_template_fields(self, structure : Structure) -> None:
        """
        Updates a structure using template field rules
        
        Parameters
        -----------
            structure : the Data Structure to update
        """
        if self.field_templates is not None : 

            ''' Remove existing field when override required'''
            for field_template in self.get_field_templates_with_existing_override_on_characterisation():
                for field_to_remove in structure.get_fields_with_characterisation(field_template.override_existing_field_on_characterisation):
                    structure.remove_field(field_to_remove.name)

            ''' Add standard field templates '''
            i=1
            for field_template in self.get_field_templates_at_start():
                field_to_add = field_template.get_field_instance()
                field_to_add.position = i
                structure.add_field(new_field=field_to_add, force_position=True)
                i+=1

            for field_template in self.get_field_templates_at_end():
                structure.add_field(new_field=field_template.get_field_instance(), force_position=False)
        
        structure.sort_fields_by_ordinal_position()
