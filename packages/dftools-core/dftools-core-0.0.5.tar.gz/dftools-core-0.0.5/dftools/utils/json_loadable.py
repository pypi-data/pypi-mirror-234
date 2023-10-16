
from typing import Dict, List
import json

from dftools.utils.dict_decoder import DictDecoderInfo, DictDecoder, create_dict_decoder

class DfJsonLoadable():
    """
        Standard Interface for a json-loadable object.
        The underlying object should extend this class and implement the methods _get_dict_decoder_info() and default_instance()
    """
    
    def __init__(self) -> None:
        pass
    
    def _get_dict_decoder_info() -> DictDecoderInfo:
        """
        Provides the DictDecoderInfo specific to the class
        This method should be overridden in each object extending
        
        Parameters
        -----------
            None

        Returns
        -----------
            The DictDecoderInfo specific to the class 
        """
        return NotImplementedError('The _get_dict_decoder_info method is not implemented')
    
    @classmethod
    def _get_dict_decoder(cls) -> DictDecoder:
        """
        Provides the DictDecoder specific to this class
        The DictDecoder is generated based on the DictDecoder provided for each object
        
        Parameters
        -----------
            None

        Returns
        -----------
            The dictionnary decoder
        """
        return create_dict_decoder(cls._get_dict_decoder_info())

    @classmethod
    def _default_instance(cls):
        """
        Returns the default instance of the class
        
        Parameters
        -----------
            None

        Returns
        -----------
            The default instance of the class
        """
        return NotImplementedError('The default_instance method is not implemented')
    
    @classmethod
    def from_dict(cls, input_dict : dict):
        """
        Loads an input dictionnary into a new instance of the class
        
        Parameters
        -----------
            input_dict : the input dictionnary containing the information of the class to load

        Returns
        -----------
            A new instance of the class loaded with all the data from the input dictionnary
        """
        return cls._get_dict_decoder()._from_dict(cls._default_instance(), input_dict)

    @classmethod
    def read_json(cls, file_path : str):
        """
        Loads into a new instance of the class the content of a file
        
        Parameters
        -----------
            file_path : the file path containing the instance information

        Returns
        -----------
            A new instance of the class loaded with all the data from the file
        """
        with open(file_path, 'r') as f:
            data_dict = json.load(f)
        return cls.from_dict(data_dict)
    