from typing import List, Dict, Tuple
import dataclasses

from dftools.core.structure import (
    Structure, 
    Field
)
from dftools.core.compare import (
    Comparator,
    ComparisonEvent,
    ComparisonDict, 
    Comparison, 
    create_comparison_event, 
    create_new_event, 
    create_remove_event
)

class StructureComparison(Comparison):
    def __init__(self
                , obj1 : Structure
                , obj2 : Structure
                , root_key_path : Tuple[str] = None
                , events: List[ComparisonEvent] = None) -> None:
        super().__init__(obj1=obj1, obj2=obj2, root_key_path=root_key_path, events=events)

    def get_sub_comparison(self, key_filter : List[str] = None):
        sub_comp_key_path = list(self.root_key_path)
        if key_filter is not None :
            sub_comp_key_path.extend(key_filter)
        sub_comp_key_path_tuple = tuple(sub_comp_key_path)
        return StructureComparison(self.obj1, self.obj2, root_key_path=sub_comp_key_path_tuple, events=self.get_sub_comparison_events(key_filter=key_filter))
    
    def get_sub_comparison_for_all_changes(self):
        """
            Get all the change events, e.g. excluding all the events without any changes
        """
        return StructureComparison(self.obj1, self.obj2, root_key_path=self.root_key_path, events=self.get_all_changes_events())
    
    def get_structure_level_key(self) -> List[str]:
        return self.root_key_path
    
    def get_structure_level_length(self) -> int:
        return len(self.get_structure_level_key())
    
    def get_events_on_structure_attributes(self) -> List[ComparisonEvent] :
        return [event for event in self.events \
                        if ( 
                            (len(event.key) >= self.get_structure_level_length() + 1) \
                            & (event.key[1] != 'fields') \
                        )]
    
    def get_comparison_of_structure_attributes(self) -> Comparison:
        return Comparison(self.obj1, self.obj2, root_key_path=self.root_key_path, events=self.get_events_on_structure_attributes())
    
    def get_field_keys(self) -> List[List[str]]:
        field_key_list = []
        for key in self.get_keys():
            if (len(key) == self.get_structure_level_length() + 2) & ('fields' in key):
                field_key_list.append(key)
        return field_key_list
    
    def get_events_on_field_attributes(self) -> Dict[Tuple[str], List[ComparisonEvent]] : 
        field_events = {}
        for field_key in self.get_field_keys():
            field_events.update({tuple(field_key) : self.get_sub_comparison_events(key_filter=field_key)})
        return field_events
    
    def get_comparison_of_fields(self) -> ComparisonDict:
        return ComparisonDict( \
                {field_event_key : Comparison(self.obj1, self.obj2, root_key_path=self.root_key_path, events=field_event_value) \
                for field_event_key, field_event_value in self.get_events_on_field_attributes().items()}
            )

class StructureComparator(Comparator[Structure, StructureComparison]):
    """
        Compare two structures. The first structure is considered as the original structure 
        and the second structure is considered as the new structure. 
    """

    def __init__(self, field_characterisation_to_check : bool = True) -> None:
        super().__init__()
        self.field_characterisation_to_check = field_characterisation_to_check

    """ Comparison methods """
    def compare(self, obj1 : Structure, obj2 : Structure, root_key_path : Tuple[str] = ()) -> StructureComparison:
        comparison_events : List[ComparisonEvent] = []
        comparison_key = obj1.name if obj1 is not None else obj2.name if obj2 is not None else ValueError('Comparator requires at least one object as original or new')
        structure_root_path = list(root_key_path)
        structure_root_path.append(comparison_key)
        comparison_events.extend(self.check_structure_events(obj1, obj2, structure_root_path))
        if (obj1 != None) & (obj2 != None):
           comparison_events.extend(self.check_all_field_changes(obj1, obj2, structure_root_path))
        return StructureComparison(obj1, obj2, root_key_path = tuple(structure_root_path), events=comparison_events)

    def check_structure_events(self, obj1 : Structure, obj2 : Structure, structure_root_path : List[str]) -> List[ComparisonEvent]:
        compare_events : List[ComparisonEvent] = []
        if (obj1 == None) & (obj2 == None):
            raise ValueError('Both structures provided are None, which is not allowed')
        if obj1 == None:
            return [create_new_event(tuple(structure_root_path), dataclasses.asdict(obj2), _type=Structure)]
        if obj2 == None:
            return [create_remove_event(tuple(structure_root_path), dataclasses.asdict(obj1), _type=Structure)]
        obj1_dict=dataclasses.asdict(obj1)
        obj2_dict=dataclasses.asdict(obj2)
        for key in ['name', 'desc', 'type', 'options', 'content_type'] :
            structure_entry_event_path = list(structure_root_path)
            structure_entry_event_path.append(key)
            compare_events.extend(create_comparison_event(tuple(structure_entry_event_path), obj1_dict[key], obj2_dict[key]))
        return compare_events

    def check_all_field_changes(self, str1 : Structure, str2 : Structure, structure_root_path : List[str]) -> List[ComparisonEvent]:
        if (str1 == None) | (str2 == None):
            return None
        compare_events : List[ComparisonEvent] = []
        field_names = list(str1.get_field_names())
        field_names.extend(name for name in str2.get_field_names() if name not in field_names)
        field_root_key=list(structure_root_path)
        field_root_key.extend(['fields'])
        for field_name in field_names:
            root_key = list(field_root_key)
            root_key.append(field_name)
            compare_events.extend(self.check_field_changes(str1.get_field(field_name), str2.get_field(field_name), root_key))
        return compare_events
    
    def check_field_changes(self, fld1 : Field, fld2 : Field, root_key : List[str]) -> List[ComparisonEvent]:
        compare_events : List[ComparisonEvent] = []
        if (fld1 == None) & (fld2 == None):
            raise ValueError('Both fields provided are None, which is not allowed')
        if fld1 == None:
            return [create_new_event(tuple(root_key), dataclasses.asdict(fld2), _type=Field)]
        if fld2 == None:
            return [create_remove_event(tuple(root_key), dataclasses.asdict(fld1), _type=Field)]
        fld1_dict=dataclasses.asdict(fld1)
        fld2_dict=dataclasses.asdict(fld2)
        field_att_to_check = ['name',  'desc', 'position', 'data_type', 'length', 'precision'
            , 'default_value']
        if self.field_characterisation_to_check :
            field_att_to_check.append('characterisations')
        for key in field_att_to_check :
            field_path = list(root_key)
            field_path.append(key)
            compare_events.extend(create_comparison_event(tuple(field_path), fld1_dict[key], fld2_dict[key]))
        return compare_events
