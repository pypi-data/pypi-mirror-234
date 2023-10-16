from dataclasses import dataclass, field
from typing import List

from dftools.utils import DictDecoderInfo, DfDataClassObj
from dftools.core.structure.core.structure_ref import StructureRef
from dftools.core.structure.core.field_characterisation import FieldCharacterisation, FieldCharacterisationStd
from dftools.core.structure.core.update_strategy import FieldUpdateStrategy

@dataclass
class FieldSourcingInfo(DfDataClassObj):

    master_source_structure_ref: StructureRef = None
    master_source_structure_field_name: str = None
    source_structure_ref: StructureRef = None
    source_structure_field_name: str = None
    field_update_strategies: List[FieldUpdateStrategy] = field(default_factory=list)
    
    def _get_dict_decoder_info() -> DictDecoderInfo:
        return DictDecoderInfo([], ["master_source_structure_ref", "master_source_structure_field_name", "source_structure_ref", "source_structure_field_name", "field_update_strategies"]
            , {"master_source_structure_ref" : StructureRef, "source_structure_ref" : StructureRef})

    @classmethod
    def _default_instance(cls):
        return cls(master_source_structure_ref=StructureRef._default_instance(), master_source_structure_field_name=''
                , source_structure_ref=StructureRef._default_instance(), source_structure_field_name=''
                , field_update_strategies = [])

    def has_master_source_structure_ref(self) -> bool:
        """
        Checks if the master source structure ref is available on this field

        Returns
        -----------
            True if the master source structure ref and field name are filled
        """
        return (self.master_source_structure_ref is not None) & (self.master_source_structure_field_name is not None)
    
    def has_source_structure_ref(self) -> bool:
        """
        Checks if the source structure ref is available on this field

        Returns
        -----------
            True if the source structure ref and field name are filled
        """
        return (self.source_structure_ref is not None) & (self.source_structure_field_name is not None)
    
    def add_field_update_strategies(self, field_update_strategies: FieldUpdateStrategy) -> None:
        """
        Adds a field update strategy to this field.
        If the field update strategy already exists, no changes are applied to the list of field update strategy.

        Returns
        -----------
            None
        """
        if field_update_strategies is not None:
            if field_update_strategies not in self.field_update_strategies:
                self.field_update_strategies.append(field_update_strategies)

@dataclass
class Field(DfDataClassObj):

    name: str
    desc: str
    position: int = 0
    data_type: str = ''
    length: int = 0
    precision: int = 0
    default_value: str = None
    characterisations: List[FieldCharacterisation] = field(default_factory=list)
    sourcing_info : FieldSourcingInfo = None

    def _get_dict_decoder_info() -> DictDecoderInfo:
        return DictDecoderInfo(["name"]
                , ["name", "desc", "position", "data_type", "length", "precision", "default_value", "characterisations", "sourcing_info"]
                , {"characterisations" : FieldCharacterisation, "sourcing_info" : FieldSourcingInfo})
    
    def __post_init__(self):
        if self.characterisations is not None : 
            if len(self.characterisations) > 0 :
                if isinstance(self.characterisations[0], dict):
                    new_char_list = []
                    for char in self.characterisations :
                        new_char_list.append(FieldCharacterisation.from_dict(input_dict=char))
                    self.characterisations = new_char_list
        
        if isinstance(self.sourcing_info, dict):
            self.sourcing_info = FieldSourcingInfo.from_dict(input_dict=self.sourcing_info)
    
    @classmethod
    def _default_instance(cls):
        return cls(name=None, desc=None, position=0, data_type='', length=0, precision=0, default_value=None
                    , characterisations=None, sourcing_info=None)

    # Characterisation methods
    def get_characterisations(self) -> List[FieldCharacterisation]:
        return self.characterisations
    
    def get_characterisation_names(self) -> List[str]:
        return [char.name for char in self.characterisations]

    def get_characterisation(self, char : str) -> FieldCharacterisation:
        for char_lcl in self.characterisations:
            if char_lcl.name == char :
                return char
    
    def has_characterisations(self) -> bool:
        """
        Checks if this field has any characterisations

        Returns
        -----------
            True if this field has any characterisations

        """
        return len(self.characterisations) > 0

    def has_characterisation(self, char : str) -> bool:
        """
        Checks if this field has the requested characterisation

        Parameters
        -----------
            char : the characterisation to look for

        Returns
        -----------
            True if this field has the characterisation searched
        """
        if char is not None :
            if char in self.get_characterisation_names():
                return True
        return False

    def add_characterisation(self, new_char : str) -> None:
        """
        Adds the characterisation provided in the characterisations of the field, if it does not already exist.
        The attributes are set to an empty dictionnary

        Parameters
        -----------
            new_char : the characterisation to be added
        """
        if new_char is not None : 
            if new_char not in self.get_characterisation_names():
                self.characterisations.append(FieldCharacterisation(name=new_char, attributes={}))
    
    def add_characterisation(self, new_char : FieldCharacterisation) -> None:
        """
        Adds the characterisation provided in the characterisations of the field, if it does not already exist

        Parameters
        -----------
            new_char : the characterisation to be added
        """
        if new_char is not None :
            if new_char.name not in self.get_characterisation_names():
                self.characterisations.append(new_char)

    def remove_characterisation(self, char : str) -> None:
        """
        Removes the characterisation provided in the characterisations of the field, if it already exist

        Parameters
        -----------
            char : the characterisation to be removed
        """
        if char is not None : 
            if char in self.get_characterisation_names():
                char_to_remove = None
                for char_lcl in self.characterisations:
                    if char_lcl.name == char:
                        char_to_remove = char_lcl
                        break
                if char_to_remove is not None :
                    self.characterisations.remove(char_to_remove)
    
    # Standard field characterisation methods
    def in_tec_key(self) -> bool:
        return self.has_characterisation(FieldCharacterisationStd.TEC_ID)
    def set_tec_key(self) -> bool:
        self.add_characterisation(FieldCharacterisationStd.TEC_ID)
    def unset_tec_key(self) -> bool:
        self.remove_characterisation(FieldCharacterisationStd.TEC_ID)
    
    def in_func_key(self) -> bool:
        return self.has_characterisation(FieldCharacterisationStd.FCT_ID)
    def set_func_key(self) -> bool:
        self.add_characterisation(FieldCharacterisationStd.FCT_ID)
    def unset_func_key(self) -> bool:
        self.remove_characterisation(FieldCharacterisationStd.FCT_ID)
    
    def is_mandatory(self) -> bool:
        return self.has_characterisation(FieldCharacterisationStd.MANDATORY)
    def set_mandatory(self) -> bool:
        self.add_characterisation(FieldCharacterisationStd.MANDATORY)
    def unset_mandatory(self) -> bool:
        self.remove_characterisation(FieldCharacterisationStd.MANDATORY)
    
    def is_unique(self) -> bool:
        return self.has_characterisation(FieldCharacterisationStd.UNIQUE)
    def set_unique(self) -> bool:
        self.add_characterisation(FieldCharacterisationStd.UNIQUE)
    def unset_unique(self) -> bool:
        self.remove_characterisation(FieldCharacterisationStd.UNIQUE)
    
    # Sourcing Info methods
    def has_sourcing_info(self) -> bool:
        """
        Checks if the sourcing info is available

        Returns
        -----------
            True if the sourcing info is available
        """
        return self.sourcing_info is not None
    
    