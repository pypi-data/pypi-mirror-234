
from typing import Dict, List

from dftools.exceptions import DfJSONValidationException

class DictDecoderInfo():
    """
        Dict Decoder standard information
    """
    def __init__(self
        , mandatory_keys : List[str] = None
        , authorized_keys : List[str] = None
        , sub_classes_map : Dict[str, type] = None
        ) -> None:
        self.mandatory_keys = mandatory_keys
        self.authorized_keys = authorized_keys
        self.sub_classes_map = sub_classes_map if sub_classes_map is not None else {}

class DictDecoder():
    """
        Standard Class to load dictionnaries into objects
    """
    def __init__(self
        , object_type : str = None
        , mandatory_keys : list = None
        , authorized_keys : list = None
        , sub_classes_map : Dict[str, type] = None
        ) -> None:
        self.object_type = object_type if object_type is not None else ''
        self.mandatory_keys = mandatory_keys
        self.authorized_keys = authorized_keys
        self.sub_classes_map = sub_classes_map if sub_classes_map is not None else {}
    
    def _check_valid_dict(self, input_dict : dict) -> bool:
        """
            Checks that the provided input dictionnary matches all the criterias :
                - All mandatory keys are present
                - Only authorized keys are present
        
            Parameters
            -----------
            input_dict : dict
                The input dictionnary

            Returns
            -----------
            True if the provided input dictionnary matches all criterias, thus is valid
            False otherwise
        """
        missing_mandatory_keys=[mandatory_key for mandatory_key in self.mandatory_keys \
            if mandatory_key not in input_dict.keys()]
        if len(missing_mandatory_keys) > 0:
            raise DfJSONValidationException(self.object_type, "Missing mandatory arguments in dictionnary", missing_mandatory_keys)
        non_authorized_keys=[key for key in input_dict.keys() if key not in self.authorized_keys]
        if len(non_authorized_keys) > 0 :
            raise DfJSONValidationException(self.object_type, "Non Authorized arguments in dictionnary", non_authorized_keys)
        return True
    
    def _from_dict(self, obj : object, input_dict : dict):
        """
            Loads an object from an input dictionnary.
            The input dictionnary is checked to be valid using the method _check_valid_dict
                
            Parameters
            -----------
            obj : object
                The object instance to be loaded. 
                WARNING : The provided object should already be instanciated.
            input_dict : dict
                The input dictionnary

            Returns
            -----------
            The object instance given as parameter with all its attributes loaded using the input dictionnary provided
        """
        self._check_valid_dict(input_dict)
        for key, value in input_dict.items():
            if not(key in self.sub_classes_map.keys()):
                setattr(obj, key, value)
            else:
                if type(value) == list:
                    current_list = []
                    for list_entry in value:
                        current_list.append(self.sub_classes_map[key].from_dict(list_entry))
                    setattr(obj, key, current_list)
                else :
                    setattr(obj, key, self.sub_classes_map[key].from_dict(value))
        return obj
    
    def _get_dict(self, obj : object) -> dict:
        """
            Get a dictionnary from an object.
                
            Parameters
            -----------
            obj : object
                The object instance to be converted to dictionnary

            Returns
            -----------
            The dictionnary description of the provided object
        """
        new_dict={}
        for key in self.authorized_keys:
            if type(obj) != dict:
                attr_obj = getattr(obj, key)
            else :
                attr_obj = obj[key] if key in obj.keys() else None

            if not(key in self.sub_classes_map.keys()):
                value = attr_obj

            else:
                if attr_obj is None:
                    value = None
                elif type(attr_obj) == list:
                    value = []
                    for list_entry in attr_obj:
                        value.append(self.sub_classes_map[key].get_dict(list_entry))

                elif type(attr_obj) == dict:
                    attr_obj : dict
                    value = {}
                    for attr_key, attr_value in attr_obj.items():
                        cur_attr_value = None
                        if type(attr_value) == list:
                            cur_attr_value = []
                            for list_entry in attr_value:
                                cur_attr_value.append(self.sub_classes_map[key].get_dict(list_entry))
                        else:
                            cur_attr_value = self.sub_classes_map[key].get_dict(attr_value)
                        value.update({attr_key : cur_attr_value})

                else :
                    value = self.sub_classes_map[key].get_dict(attr_obj)
            new_dict.update({key : value})

        return new_dict


def create_dict_decoder(info : DictDecoderInfo) -> DictDecoder :
    return DictDecoder(mandatory_keys = info.mandatory_keys, authorized_keys = info.authorized_keys, sub_classes_map = info.sub_classes_map)