
import os
from typing import Any, Dict
from dftools.utils.file_util import get_list_of_files_in_cur_folder

def load_json_files_into_dict(folder_path : str, file_pattern : str, associated_type : type) -> Dict[str, Any]:
  """
    Load JSON files into a new dictionnary

    Parameters
    -----------
    folder_path : str
      The folder path to look into
    file_pattern : str
      The file pattern to match
    associated_type : type
      The assocaited type to the json files to read

    Returns
    -----------
    A loaded dictionnary from the list of files in the provided directory 
    and matching the provided file pattern
  """
  output_dict={}
  if os.path.exists(folder_path) :
    for file_path in get_list_of_files_in_cur_folder(folder_path, file_pattern):
      model_object = associated_type.read_json(file_path)
      output_dict.update({model_object.name : model_object})
  return output_dict