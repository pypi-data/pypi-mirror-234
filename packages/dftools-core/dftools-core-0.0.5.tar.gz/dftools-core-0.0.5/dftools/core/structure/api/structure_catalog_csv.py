from typing import List, Tuple

from dftools.events import log_event
from dftools.utils import CsvLoader
from dftools.core.structure.core import StructureCatalog, Structure, Field, Namespace, FieldCharacterisation
from dftools.events.events import CSVFileReadSuccessful

class StructureCatalogCsv(CsvLoader[StructureCatalog, Tuple[Namespace, Structure]]):
    
    @classmethod
    def _get_csv_input_parameters(cls) -> dict:
        return {
            "first_element" : "Data Structure"
            , "row_type_column_position" : 5
            , "row_types" : {
                "Data Structure" : {"name" : "data_structure", "method_rule" : "cls._create_structure_from_row(row)"}
                , "Field Structure" : {"name" : "field_structure", "method_rule" : "cls._create_field_from_row(row)"}
            }
        }
    
    @classmethod
    def get_header_row_list(cls) -> List[str]:
        return [ 'DataBank', 'Catalog', 'Namespace', 'Structure Name'
            , 'Structure Type', 'Row Type', 'Position', 'Field Name'
            , 'Description', 'Characterisations', 'DataType', 'Length'
            , 'Precision', 'Default Value']
    
    # Object Array creation methods for csv write operations

    @classmethod
    def format_object_to_array(cls, obj : StructureCatalog) -> list:
        output_list = []
        for namespace, structure_dict in obj.structures.items():
            for structure in list(structure_dict.values()):
                output_list.extend(cls.format_structure_to_array(namespace, structure))
        return cls.clean_object_arrays(obj_arrays=output_list)

    @classmethod
    def format_structure_to_array(cls, namespace : Namespace, obj : Structure) -> List[list]:
        """ 
        Get a description of the structure as a list,
        with the first element the description of the structure
        and the following the description of the fields

        Returns
        -----------
            A list of elements
        """
        structure_list=[]

        ''' Add an entry for the structure level'''
        structure_list.append([
            namespace.databank_name
            , namespace.catalog
            , namespace.namespace
            , obj.name
            , obj.type
            , 'Data Structure'
            , None
            , None
            , obj.desc
            , None
            , None
            , obj.row_count
        ])

        ''' Add one entry per field in the the structure level'''
        for field in obj.fields:
            field : Field
            structure_list.append([
                  namespace.databank_name
                , namespace.catalog
                , namespace.namespace
                , obj.name
                , obj.type
                , 'Field Structure'
                , field.position
                , field.name
                , field.desc
                , ','.join([char.name for char in field.characterisations])
                , field.data_type
                , field.length
                , field.precision
                , field.default_value
            ])
        return structure_list
    
    @classmethod
    def get_max_data_columns(cls) -> int:
        return 20
    
    @classmethod
    def read_csv(cls, file_path : str, newline : str = '', delimiter : str = ';', quotechar : str = '"'
        , encoding : str = 'ISO 8859-1') -> StructureCatalog:
        str_catalog = StructureCatalog()
        for object_dict in cls.read_csv_to_list_from_file(file_path=file_path, newline=newline, delimiter=delimiter
            , quotechar=quotechar, encoding=encoding):
            namespace, structure = cls._create_object_from_rows(**object_dict)
            for field in structure.fields :
                csv_characterisations : List[str] = field.characterisations
                if csv_characterisations is not None:
                    if len(csv_characterisations) > 0:
                        new_char_list = []
                        for csv_char in csv_characterisations:
                            new_char_list.append(FieldCharacterisation(name=csv_char, attributes=None))
                        field.characterisations = new_char_list
            str_catalog.add_structure(namespace, structure)
        log_event(None, CSVFileReadSuccessful(file_path=file_path, object_type_name='Structure Catalog'))
        return str_catalog

    # Create objects methods from string / input array

    @classmethod
    def _create_object_from_rows(cls, **kwargs) -> Tuple[Namespace, Structure]:
        namespace : Namespace = kwargs['data_structure'][0][0]
        data_structure : Structure = kwargs['data_structure'][0][1]
        field_structures = kwargs['field_structure'] if 'field_structure' in kwargs else []
        for field_structure in field_structures:
            data_structure.add_field(field_structure)
        return (namespace, data_structure)

    @classmethod
    def _create_structure_from_row(cls, row : List[str]) -> Tuple[Namespace, Structure]:
        cls.clean_object_array(row)
        return (
            Namespace(row[0], row[1], row[2])
            , Structure(
                name = row[3]
                , desc = row[8]
                , type = row[4]
                , row_count = cls._get_int_from_single_cell(row[11])
                , options= {}
                , content_type = []
                , fields = []
                , sourcing_info = None
            )
        )
    
    @classmethod
    def _create_field_from_row(cls, row : List[str]):
        cls.clean_object_array(row)
        return Field(
            name=row[7]
            , desc=row[8]
            , position=cls._get_int_from_single_cell(row[6])
            , characterisations=cls._get_list_from_single_cell(row[9])
            , data_type=row[10].upper() if row[10] is not None else None
            , length=cls._get_int_from_single_cell(row[11])
            , precision=cls._get_int_from_single_cell(row[12])
            , default_value=row[13] if (row[13] is not None) & (row[13].strip() != '') else None
            , sourcing_info=None
        )
