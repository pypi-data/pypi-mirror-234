
import os
from typing import List, Tuple

from dftools.core.database.query_result import QueryExecResult

def write_script_execution_result_to_file(script_results : List[Tuple[str, QueryExecResult]], file_path : str) -> None:
    with open(file_path, "w") as output_file:
        for script_result in script_results :
            output_file.write(os.path.basename(script_result[0]) + ' : ' + script_result[1].get_status())
            output_file.write("\n")
