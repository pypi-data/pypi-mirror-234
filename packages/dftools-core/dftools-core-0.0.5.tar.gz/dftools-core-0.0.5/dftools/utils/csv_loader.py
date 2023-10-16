import csv
from typing import List, TypeVar, Generic

from dftools.events import log_event
from dftools.events.events import CSVFileWriteSuccessful

C = TypeVar("C")
T = TypeVar("T")

class CsvLoader(Generic[C, T]):
    """
        Standard Class to read/write csv files
    """
    def __init__(self) -> None:
        pass
    
    @classmethod
    def _get_csv_input_parameters(cls) -> dict:
        return NotImplementedError('The _get_csv_input_parameters method is not implemented')
    
    @classmethod
    def _get_csv_row_types(cls) -> str:
        return cls._get_csv_input_parameters()["row_types"]
    
    @classmethod
    def _get_csv_row_first_element(cls) -> str:
        return cls._get_csv_input_parameters()["first_element"]

    @classmethod
    def _get_csv_row_type_column_position(cls) -> str:
        return cls._get_csv_input_parameters()["row_type_column_position"]

    @classmethod
    def read_csv(cls, file_path : str, newline : str = '', delimiter : str = ';', quotechar : str = '"'
        , encoding : str = 'ISO 8859-1') -> C:
        return NotImplementedError('The read_csv method is not implemented')

    @classmethod
    def _create_object_from_rows(**kwargs) -> T:
        return NotImplementedError('The _create_object_from_rows method is not implemented')

    @classmethod
    def read_csv_to_list(cls, content : str, delimiter : str = ';', quotechar : str = '"') -> list:
        """
        Reads csv format with the standard description of structures and returns a list of the class
        
        Parameters
        -----------
            file_path : the csv data dictionnary file path
            newline : the newline string describing the file, defaulted to "" (empty string)
            delimiter : the delimiter string describing the file, defaulted to ";"
            quotechar : the quotechar string describing the file, defaulted to "\"" (double quote)
            encoding : the encoding of the file to read

        Returns
        -----------
            A list of objects based on the data available in the csv file
        """
        row_type_column=cls._get_csv_row_type_column_position()
        row_types=cls._get_csv_row_types()
        first_row_type=cls._get_csv_row_first_element()
        objects_read=[]
        current_object={}
        
        reader = csv.reader(content.splitlines(), delimiter=delimiter, quotechar=quotechar)
        i=0
        for row in reader:
            row_type = row[row_type_column]
            if str(row_type) ==  first_row_type:
                if i != 0 : 
                    objects_read.append(current_object)
                current_object = {}
            row_type_info = row_types[row_type]
            current_row_type_name = row_type_info['name']
            new_object = eval(row_type_info['method_rule'])
            if current_row_type_name in current_object.keys():
                current_list : list=current_object[current_row_type_name]
                current_list.append(new_object)
            else :
                current_object.update({current_row_type_name : [new_object]})
            i+=1
        
        # After the read, add the last found structure to the structures read
        objects_read.append(current_object)
        return objects_read
    
    @classmethod
    def read_csv_to_list_from_file(cls, file_path : str, newline : str = '', delimiter : str = ';', quotechar : str = '"'
        , encoding: str = 'ISO 8859-1') -> list:
        """
        Reads csv format with the standard description of structures and returns a list of the class
        
        Parameters
        -----------
            file_path : the csv data dictionnary file path
            newline : the newline string describing the file, defaulted to "" (empty string)
            delimiter : the delimiter string describing the file, defaulted to ";"
            quotechar : the quotechar string describing the file, defaulted to "\"" (double quote)
            encoding : the encoding of the file to read

        Returns
        -----------
            A list of objects based on the data available in the csv file
        """
        row_type_column=cls._get_csv_row_type_column_position()
        row_types=cls._get_csv_row_types()
        first_row_type=cls._get_csv_row_first_element()
        objects_read=[]
        current_object={}
        with open(file_path, newline=newline, encoding=encoding) as csvfile:
            next(csvfile)
            reader = csv.reader(csvfile, delimiter=delimiter, quotechar=quotechar)
            i=0
            for row in reader:
                row_type = row[row_type_column]
                if str(row_type) ==  first_row_type:
                    if i != 0 : 
                        objects_read.append(current_object)
                    current_object = {}
                row_type_info = row_types[row_type]
                current_row_type_name = row_type_info['name']
                new_object = eval(row_type_info['method_rule'])
                if current_row_type_name in current_object.keys():
                    current_list : list=current_object[current_row_type_name]
                    current_list.append(new_object)
                else :
                    current_object.update({current_row_type_name : [new_object]})
                i+=1
            
            # After the read, add the last found structure to the structures read
            objects_read.append(current_object)
        return objects_read

    @classmethod
    def get_header_row_list(cls) -> List[str]:
        return NotImplementedError('The get_header_row_list method is not implemented')

    @classmethod
    def format_object_to_array(cls, obj : T) -> list:
        return NotImplementedError('The format_object_to_array method is not implemented')
    
    @classmethod
    def get_max_data_columns(cls) -> int:
        return NotImplementedError('The get_max_data_columns method is not implemented')
    
    @classmethod
    def clean_object_arrays(cls, obj_arrays : List[list]) -> List[list]:
        # Ensure all the items in the output list contains the maximum expected of data columns.
        # If that's not the case, extend the list
        for output_entry in obj_arrays:
            cls.clean_object_array(output_entry)
        return obj_arrays
    
    @classmethod
    def clean_object_array(cls, obj_array : list) -> list:
        # Ensure all the items in the output list contains the maximum expected of data columns.
        # If that's not the case, extend the list
        if len(obj_array) < cls.get_max_data_columns():
            obj_array.extend([None]*(cls.get_max_data_columns()-len(obj_array)))
        return obj_array
    
    @classmethod
    def to_csv(cls, file_path : str, obj : T, newline : str = '', delimiter : str = ';', quotechar : str = '"') -> None:
        """
        Writes to a csv file format
        
        Parameters
        -----------
            file_path : the csv file path
            newline : the newline string describing the file, defaulted to "" (empty string)
            delimiter : the delimiter string describing the file, defaulted to ";"
            quotechar : the quotechar string describing the file, defaulted to "\"" (double quote)

        """
        with open(file_path, 'w', newline=newline) as csvfile:
            writer = csv.writer(csvfile, delimiter=delimiter, quotechar=quotechar)
            # Header row
            writer.writerow(cls.get_header_row_list())
            # Data row
            for row in cls.format_object_to_array(obj):
                writer.writerow(row)
        log_event(None, CSVFileWriteSuccessful(file_path=file_path, object_type_name=str(type(obj))))
    
    # Read / Write Methods
    
    def _get_list_from_single_cell(input_str : str, delimiter : str = ',') -> list:
        return [entry.strip() for entry in input_str.split(delimiter) if entry.strip() != '']
    
    def _get_int_from_single_cell(input_str : str) -> int:
        return int(input_str) if (input_str is not None) & (input_str.strip() != '') else None
    
    def _get_int_from_bool_single_cell(input_str : str) -> int:
        if input_str is None:
            return False
        if input_str == '':
            return False
        return True if int(input_str) == 1 else False

    def _get_nullable_string_from_single_cell(input_str : str) -> str:
        return input_str if input_str != '' else None

    def _get_str_from_str_single_cell(input_str : str) -> str:
        if input_str is None:
            return None
        if input_str.strip() == '':
            return None
        return input_str