from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime
    
@dataclass
class QueryExecResult():
    """
        Query Result
        All the queries returned by the method execute_query should return this object
    """
    query_name : str
    exec_status : str
    query : str
    query_id : str
    result_set : Optional[list]
    result_set_structure : Optional[list]
    start_tst : datetime
    end_tst : datetime
    
    SUCCESS = 'SUCCESS'
    ERROR = 'ERROR'

    # Status methods
    def is_success(self) -> bool:
        return self.exec_status == self.SUCCESS
    
    def is_error(self) -> bool:
        return self.exec_status == self.ERROR
    
    def get_error_message(self) -> str:
        if self.is_error():
            if self.result_set is not None:
                return self.result_set[0].replace('\n', ' ').replace('\r', ' ').strip()
        return ''
            
    # Dictionnary methods
    
    def to_dict(self) -> dict:
        return {
              "query_name" : self.query_name
            , "exec_status" : self.exec_status
            , "query" : self.query
            , "query_id" : self.query_id
            , "result_set" : self.result_set
            , "result_set_header" : self.result_set_structure
            , "start_tst" : self.start_tst.strftime("%Y%m%d%H%M%S%f")
            , "end_tst" : self.end_tst.strftime("%Y%m%d%H%M%S%f")
        }


class QueryExecResults(List[QueryExecResult]):
    def __init__(self) -> None:
        super().__init__()
    
    def get_status(self) -> str:
        if self.has_succeeded():
            return QueryExecResult.SUCCESS
        return QueryExecResult.ERROR
            
    def has_succeeded(self) -> bool:
        for query_exec_result in self:
            if query_exec_result.is_error():
                return False
        return True
    
    def has_failed(self) -> bool:
        for query_exec_result in self :
            if query_exec_result.is_error():
                return True
        return False
    
    def get_number_of_results(self) -> int:
        return len(self)

    def to_str(self) -> str:
        return ', '.join([str(query_exec_result.to_dict()) for query_exec_result in self])
    
    def report_exec_status(self) -> str:
        return '\n'.join([(query_exec_result.query_name if query_exec_result.query_name is not None else '') + ' : ' 
            + query_exec_result.exec_status  + ('(' + query_exec_result.get_error_message() + ')' if query_exec_result.is_error() else '')
            for query_exec_result in self])

    def report_to_csv(self, delimiter : str = ';', new_line : str = '\n') -> str:
        report_list = [['Query Name', 'Execution Status', 'Execution Message']]
        for query_exec_result in self:
            report_list.append([query_exec_result.query_name, query_exec_result.exec_status, query_exec_result.get_error_message()])
        return new_line.join([delimiter.join(report_row) for report_row in report_list])
