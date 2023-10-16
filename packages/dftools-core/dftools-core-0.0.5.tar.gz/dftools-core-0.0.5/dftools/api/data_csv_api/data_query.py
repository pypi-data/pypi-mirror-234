import os
from typing import List

import pandas as pd
from jinja2 import Template

from dftools.events import log_event_default, StandardInfoEvent as StdInfoEvent
from dftools.core.structure import StructureCatalog, StructureCatalogCsv

def create_statement_from_data_files(
        folder_path : str
        , structure_name : str
        , template_file_path : str
        , target_structure_name : str = None
        , files_prefix : str = ""
        , files_suffix : str = ""
        , data_file_encoding : str = 'ISO-8859-1'
        , field_characterisations_to_exclude : List[str] = None
        , output_folder_path : str = None) -> str:
    """Creates a statement from the data files provided using the provided template file.

    The template is rendered using the information :
    - structure_name : the name of the structure name to be used in the statement
    - data_sample : the data full sample from the data file
    - str_field_names : the list of field names available in the data sample in the order of the columns in data_sample

    This method requires 3 input files :
    - The template file
    - The structure metadata file, which should be named using the pattern "structure_name + files_prefix + '.metadata.csv'"
    - The csv data file, which should be named using the pattern "structure_name + files_prefix + '.' + files_suffix + '.csv'" and encoded in ISO-8859-1
    
    Parameters
    ----------
    folder_path : str
        The folder path containing all the input files
    structure_name : str
        The structure name
    template_file_path : str
        The template file path
    files_prefix : str, optional
        The prefix on all the files
    files_suffix : str, optional
        The suffix on all the data files
    data_file_encoding : str, optional
        The encoding of the data file, defaulted to ISO-8859-1
    field_characterisations_to_exclude : List[str], optional
        The list of field characterisations to exclude from the output
    output_folder_path : str, optional
        The output folder path. If not provided, no output is generated.

    Returns
    ----------
    statement : str
        The statement of manual data rendered using the provided template
    """
    
    folder_abs_path = os.path.abspath(folder_path)
    field_characterisations_to_exclude = \
        ['REC_DELETION_TST','REC_DELETION_USER_NAME','REC_INSERT_TST','REC_INSERT_USER_NAME','REC_LAST_UPDATE_TST','REC_LAST_UPDATE_USER_NAME'] \
            if field_characterisations_to_exclude is None else field_characterisations_to_exclude
    
    str_catalog : StructureCatalog = StructureCatalogCsv.read_csv(os.path.join(folder_abs_path, structure_name + files_prefix + '.metadata.csv'))
    structure = str_catalog.get_structure_by_name(structure_name)
    df = pd.read_csv(
        os.path.join(folder_abs_path, structure_name + files_prefix + '.' + files_suffix + '.csv')
        , sep=";" 
        , encoding = data_file_encoding
        , keep_default_na = False)

    df_for_statement = df[structure.get_field_names_wo_characterisations(field_characterisations_to_exclude)]

    data_for_template = {
        "structure_name" : "DUMMY_" + structure_name.upper() if target_structure_name is None else target_structure_name
        , "data_sample" : df_for_statement.values.tolist()
        , "str_field_names" : structure.get_field_names_wo_characterisations(field_characterisations_to_exclude)
    }

    with open(template_file_path, 'r') as file:
        template_file = file.read()
    template = Template(template_file)
    statement = template.render(data_for_template)

    if output_folder_path is not None :
        os.makedirs(output_folder_path, exist_ok=True)
        output_file_path = os.path.abspath(os.path.join(output_folder_path, data_for_template['structure_name'] + '.sql'))
        with open(output_file_path, "w") as fh:
            fh.write(statement)
        log_event_default(StdInfoEvent('Manual Data File generated at location : ' + output_file_path))

    return statement