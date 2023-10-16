
from typing import Dict
from dftools.core.structure.core import Field

class BaseFieldDecoder:
    """ Field - Base Decoder - Main class to inherit"""
    
    def __init__(self):
        pass

    def decode_json(self, input_data : Dict[str, str]) -> Field :
        """ 
        Decodes the provided json dictionnary into a field
        
        Parameters
        -----------
        input_data : dict
            The field data dictionnary to be decoded

        Returns
        -----------
            The newly created Field based on the provided dictionnary
        """
        raise NotImplementedError('`decode_json` should be implemented in field decoder')

class StdFieldDecoder(BaseFieldDecoder):
    """ Field - Standard Decoder - Main class to inherit"""

    def __init__(self) -> None:
        pass

    def decode_json(self, input_data: Dict[str, str]) -> Field:
        return Field.from_dict(input_dict=input_data)
