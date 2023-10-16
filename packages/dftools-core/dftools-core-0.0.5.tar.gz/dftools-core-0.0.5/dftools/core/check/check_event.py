import csv

from typing import List, Dict
from dftools.events import log_event
from dftools.events.events import CSVFileWriteSuccessful

class CheckInfo():

    """ Check status """
    VALID='VALID'
    WARN='WARN'
    ERROR='ERROR'

    def __init__(self
        , status : str
        , desc : str = None) -> None :
        self.status = status
        self.desc = desc

    """ Check Status """
    def is_valid(self) -> bool:
        return self.status == CheckInfo.VALID
    def is_warn(self) -> bool:
        return self.status == CheckInfo.WARN
    def is_error(self) -> bool:
        return self.status == CheckInfo.ERROR
    def is_not_valid(self) -> bool:
        return self.status != CheckInfo.VALID
    def is_not_error(self) -> bool:
        return self.status != CheckInfo.ERROR

class ValidCheckInfo(CheckInfo):
    def __init__(self, desc: str = None) -> None:
        super().__init__(CheckInfo.VALID, desc)

class WarnCheckInfo(CheckInfo):
    def __init__(self, desc: str = None) -> None:
        super().__init__(CheckInfo.WARN, desc)

class ErrorCheckInfo(CheckInfo):
    def __init__(self, desc: str = None) -> None:
        super().__init__(CheckInfo.ERROR, desc)

class CheckEvent(CheckInfo):
    def __init__(self
        , rule_name : str
        , root_key : str
        , key : str
        , status : str
        , desc : str
        ) -> None:
        super().__init__(status, desc)
        self.rule_name = rule_name
        self.root_key = root_key
        self.key = key

    def get_result(self) -> str:
        return self.key + ' / ' + self.rule_name + ' / ' + self.status \
            + ((' (' + self.desc + ')' ) if self.status != CheckInfo.VALID else '')

class CheckResult():
    def __init__(self
        , obj = None
        , checks : list = None
        ) -> None:
        self.checked_obj = obj
        self.check_events : List[CheckEvent] = []
        if checks is not None :
            for check in checks:
                    self.check_events.append(check)
    
    def add_check(self, check_event : CheckEvent):
        self.check_events.append(check_event)

    def get_checks(self) -> List[CheckEvent] :
        checks=[]
        checks.extend(self.check_events)
        return checks

    def get_checks_by_key(self, key : str) -> List[CheckEvent]:
        return [check for check in self.get_checks() if check.key == key]

    def get_check_events(self) -> List[CheckEvent]:
        return self.check_events

    def get_checks_by_status(self, status : str) -> List[CheckEvent] :
        checks=[]
        for check_event in self.check_events: 
            if check_event.status == status:
                    checks.append(check_event)
        return checks

    def get_check_keys(self) -> list:
        keys=[check_event.key for check_event in self.get_checks()]
        return list(dict.fromkeys(keys))

    def get_check_summary_by_key(self) -> list:
        check_summary=[]
        for key in self.get_check_keys():
            cur_check_wrapper=CheckResult(checks=self.get_checks_by_key(key))
            cur_summary={}
            cur_summary['key'] = key
            cur_summary['summary'] = {
                "VALID": len(cur_check_wrapper.get_checks_by_status(CheckInfo.VALID))
                , "WARN": len(cur_check_wrapper.get_checks_by_status(CheckInfo.WARN))
                , "ERROR": len(cur_check_wrapper.get_checks_by_status(CheckInfo.ERROR))
            }
            check_summary.append(cur_summary)
        return check_summary

    def get_check_summary(self) -> Dict[str, int]:
        return {
            "VALID": len(self.get_checks_by_status(CheckInfo.VALID))
            , "WARN": len(self.get_checks_by_status(CheckInfo.WARN))
            , "ERROR": len(self.get_checks_by_status(CheckInfo.ERROR))
        }

    def report(self) -> list:
        return [check.get_result() for check in self.get_checks()]

    def report_errors(self) -> list:
        return [check.get_result() for check in self.get_checks() if check.is_error()]

    def to_csv(self, file_path : str, newline : str = '', delimiter : str = ';', quotechar : str = '"') -> None:
        with open(file_path, 'w', newline=newline) as csvfile:
            writer = csv.writer(csvfile, delimiter=delimiter, quotechar=quotechar)
            # Header row
            writer.writerow(['Root Key', 'Key', 'Rule Name', 'Status', 'Desc'])
            # Data row
            for check_event in self.check_events:
                writer.writerow([check_event.root_key, check_event.key, check_event.rule_name, check_event.status, check_event.desc])
        log_event(None, CSVFileWriteSuccessful(file_path=file_path, object_type_name=CheckResult.__name__))

class CheckResults(List[CheckResult]):
    def __init__(self) -> None:
        pass

    def to_csv(self, file_path : str, newline : str = '', delimiter : str = ';', quotechar : str = '"') -> None:
        with open(file_path, 'w', newline=newline) as csvfile:
            writer = csv.writer(csvfile, delimiter=delimiter, quotechar=quotechar)
            # Header row
            writer.writerow(['Root Key', 'Key', 'Rule Name', 'Status', 'Desc'])
            # Data row
            for check_result in self:
                for check_event in check_result.check_events:
                    writer.writerow([check_event.root_key, check_event.key, check_event.rule_name, check_event.status, check_event.desc])
        log_event(None, CSVFileWriteSuccessful(file_path=file_path, object_type_name=CheckResult.__name__))