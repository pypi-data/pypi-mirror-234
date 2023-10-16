
import regex as re

from dftools.core.check.check_event import CheckInfo, ValidCheckInfo, ErrorCheckInfo
from dftools.core.check.check_rule import CheckRule

class RegexCheckRule(CheckRule) :
    def __init__(self, name: str, pattern : str, local_dictionary : dict = None) -> None:
        super().__init__(name, authorized_obj_class=[str], none_checkable=False)
        self.pattern = pattern
        self.local_dictionary = local_dictionary if local_dictionary is not None else {}
   
    def _check_obj(self, obj : str) -> CheckInfo:
        p = re.compile(pattern=self.pattern, **self.local_dictionary)
        p_fullmatch = p.fullmatch(obj)
        if p_fullmatch is not None:
            return ValidCheckInfo()
        return ErrorCheckInfo(desc=f'String {obj} is not matching the pattern {self.pattern}')