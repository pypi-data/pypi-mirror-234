
import os
import logging
from typing import Any, Dict, List

from dftools.events import log_event
from dftools.events.events import ConfigurationFileLoadCompleted, ConfigurationMissingFolder
from dftools.utils.dict_loader_util import load_json_files_into_dict

class ObjReadHelper():
    def __init__(self, object_type_name : str, are_system_files : bool, folder_name : str, file_pattern : str, object_type : type) -> None:
        self.object_type_name = object_type_name
        self.are_system_files = are_system_files
        self.folder_name = folder_name
        self.file_pattern = file_pattern if file_pattern is not None else "[a-zA-Z_]*.json"
        self.object_type = object_type

class ObjectStandardProviderService():
    """
        Standard Object Provider Service
    """
    def __init__(self, system_folder : str, user_folder : str, object_read_helper_dict : Dict[str, ObjReadHelper]) -> None:
        self.objects={}
        self.logger = logging.getLogger(__name__)
        self.system_folder = system_folder
        self.user_folder = user_folder
        self.object_read_helper_dict = object_read_helper_dict        

    def replace_object_type_objects(self, key : str, obj_dict : Dict[str, Any]):
        self.objects.update({key : obj_dict})

    def load_json_files_into_service(self, obj_read_helper : ObjReadHelper):
        root_folder_path = self.system_folder if obj_read_helper.are_system_files else self.user_folder
        folder_complete_path = os.path.join(root_folder_path, obj_read_helper.folder_name)
        if not os.path.exists(folder_complete_path):
            ConfigurationMissingFolder(object_type_name=obj_read_helper.object_type_name, folder_path=folder_complete_path)
            self.replace_object_type_objects(obj_read_helper.object_type_name, {})
        else :
            self.replace_object_type_objects(obj_read_helper.object_type_name
                , load_json_files_into_dict(folder_complete_path, obj_read_helper.file_pattern, obj_read_helper.object_type))
        log_event(self.logger, ConfigurationFileLoadCompleted(object_type_name=obj_read_helper.object_type_name, folder_path=folder_complete_path))
        
    def load_objects_from_files(self):
        for obj_read_helper in self.object_read_helper_dict.values():
            self.load_json_files_into_service(obj_read_helper)

    def get_available_object_types(self) -> List[str]:
        """ 
        Get all the available object types.
        
        Returns
        -----------
            The string-list of object types
        """
        return list(self.objects.keys())
    
    def get_object_dict(self) -> Dict[str, Dict[str, Any]]:
        """ 
        Get the complete object Dictionnary.

        The dictionnary associates a object type name (key) to a dictionnary 
        containing all the objects stored with a key name
        
        Returns
        -----------
            The object dictionnary
        """
        return self.objects
    
    def get_dict(self, object_type : str) -> Dict[str, Any]:
        """ 
        Get a key-value dictionnary for the object type provided.

        The key is the name of the object and the value can be 
        of any type but always the same throughout the dictionnary.
        
        Parameters
        -----------
            object_type : the name of the object type

        Returns
        -----------
            The object type dictionnary
        """
        return self.objects[object_type] if object_type in self.objects.keys() else {}
    
    def get_object_keys(self, object_type : str) -> List[str]:
        """ 
        Get the list of keys for the object type provided.
        
        Parameters
        -----------
            object_type : the name of the object type

        Returns
        -----------
            The list of keys for the object type provided
        """
        return self.get_dict(object_type).keys()

    def get_object(self, object_type : str, object_key : str) -> Any :
        """ 
        Get the object of type object_type and with name equal to the object_key
        
        Parameters
        -----------
            object_type : the name of the object type
            object_key : the key (name) of the object

        Returns
        -----------
            A stored object
        """
        obj_type_dict = self.get_dict(object_type=object_type)
        if obj_type_dict is None : 
            raise ValueError('No Object Type stored with name : ' + object_type)
        return obj_type_dict[object_key] if object_key in obj_type_dict.keys() else None
    
    def get_objects(self, object_type : str, object_keys : List[str]) -> List[Any] :
        """ 
        Get the list of objects of type object_type and with the object keys (names) as provided
        
        Parameters
        -----------
            object_type : the name of the object type
            object_keys : the list of keys (names) of the objects to look for

        Returns
        -----------
            The list of stored objects with the provided keys
        """
        obj_type_dict = self.get_dict(object_type=object_type)
        if obj_type_dict is None : 
            raise ValueError('No Object Type stored with name : ' + object_type)
        return [obj_type_dict[key] for key in object_keys if key in obj_type_dict.keys()]
    
    def get_objects_as_dict(self, object_type : str, object_keys : List[str]) -> Dict[str, Any] :
        """ 
        Get the list of objects of type object_type and with the object keys (names) as provided in a dict format
        
        Parameters
        -----------
            object_type : the name of the object type
            object_keys : the list of keys (names) of the objects to look for

        Returns
        -----------
            The list of stored objects with the provided keys as a dictionnary with as key the object name/key
        """
        obj_type_dict = self.get_dict(object_type=object_type)
        if obj_type_dict is None : 
            raise ValueError('No Object Type stored with name : ' + object_type)
        return {key : obj_type_dict[key] for key in object_keys if key in obj_type_dict.keys()}