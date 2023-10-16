
import json
from typing import Dict

from dftools.core.structure.decoder.field_decoder import BaseFieldDecoder, StdFieldDecoder
from dftools.core.structure.core import Namespace, Structure, StructureCatalog

class BaseStructureDecoder:
    """ Structure - Base Decoder - Main class to inherit"""
    
    def __init__(self, field_decoder : BaseFieldDecoder):
        self.field_decoder = field_decoder

    def decode_json(self, input_data : Dict[str, str]) -> (Namespace, Structure) :
        """ 
        Decodes the provided json dictionnary into a structure
        
        Parameters
        -----------
        input_data : dict
            The structure data dictionnary to be decoded

        Returns
        -----------
            The newly created Structure based on the provided dictionnary
        """
        raise NotImplementedError('`decode_json` should be implemented in structure decoder')

    def decode_json_from_file(self, file_path : str) -> (Namespace, Structure):
        """ 
        Decodes the provided file into a Structure
        
        Parameters
        -----------
        file_path: str
            The file path containing the data structure description

        Returns
        -----------
            The newly created Structure based on the provided dictionnary
        """
        with open(file_path, 'r') as myfile:
            data=myfile.read()
        return self.decode_json(data_structure_data=json.loads(data))
    

class StdStructureDecoder(BaseStructureDecoder):
    def __init__(self):
        super().__init__(StdFieldDecoder())
    
    def decode_json(self, input_data: Dict[str, str]) -> (Namespace, Structure):
        return (Namespace(None, None, None), Structure.from_dict(input_dict=input_data))

class StructureCatalogDecoder:
    """ Structure Catalog - Decoder - Standard"""

    def __init__(self) -> None:
        pass

    def __init__(self, structure_decoder : BaseStructureDecoder):
        self.structure_decoder = structure_decoder

    def decode_json(self, input_data : dict) -> StructureCatalog:
        """ 
        Decodes the provided json dictionnary into a structure catalog
        
        Parameters
        -----------
        input_data : dict
            The structure catalog data dictionnary to be decoded

        Returns
        -----------
            The newly created Structure Catalog based on the provided dictionnary
        """
        namespace = Namespace(databank_name=input_data['databank_name'], catalog=input_data['catalog'], namespace=input_data['namespace'])
        structures : Dict[str, Structure] = {}
        for structure_data in input_data['STRUCTURES']:
            structure = self.structure_decoder.decode_json(input_data=structure_data)
            structures[structure.name] = structure
        return StructureCatalog({namespace : structures})

    def decode_json_from_file(self, file_path : str) -> StructureCatalog:
        """ 
        Decodes the provided file into a DataStructureList
        
        Parameters
        -----------
        file_path: str
            The file path containing the data structure description

        Returns
        -----------
            The newly created DataStructureList based on the provided dictionnary
        """
        with open(file_path, 'r') as myfile:
            data=myfile.read()
        return self.decode_json(input_data=json.loads(data))

