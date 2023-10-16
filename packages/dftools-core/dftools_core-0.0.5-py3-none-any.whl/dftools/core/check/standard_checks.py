
from dftools.core.check.check_rule import StdSimpleCheckRule, StdSimpleWarnCheckRule

class StringValuedCheck(StdSimpleCheckRule):
    def __init__(self, name: str = 'String is valued', err_msg : str = 'String is not valued') -> None:
        super().__init__(name=name, err_msg=err_msg, authorized_obj_class=[str], none_checkable=True)

    def _check_obj_rule(self, obj : str) -> bool:
        return (obj is not None) & (obj != '')

class ListIsNotEmptyCheck(StdSimpleCheckRule):
    def __init__(self, name: str = 'List is not empty', err_msg : str = 'List is empty') -> None:
        super().__init__(name=name, err_msg=err_msg, authorized_obj_class=[list], none_checkable=True)

    def _check_obj_rule(self, obj : list) -> bool:
        return (obj is not None) & (len(obj) > 0)

class ListIsNotEmptyWarnCheck(StdSimpleWarnCheckRule):
    def __init__(self, name: str = 'List is not empty', err_msg : str = 'List is empty') -> None:
        super().__init__(name=name, err_msg=err_msg, authorized_obj_class=[list], none_checkable=True)

    def _check_obj_rule(self, obj : list) -> bool:
        return (obj is not None) & (len(obj) > 0)

class ListContainsMandatoryValuesCheck(StdSimpleCheckRule):
    def __init__(self, name: str = 'List contains the mandatory values'
        , err_msg : str = 'List does not contain all of the mandatory values'
        , expected_values : list = None
        , err_value_delimiter : str = ', ') -> None:
        if expected_values is None:
            raise ErrorValue('The expected values cannot be None')
        if len(expected_values) == 0:
            raise ErrorValue('The expected values cannot be empty')
        self.expected_values = expected_values
        super().__init__(name=name, err_msg=err_msg + ' : ' + err_value_delimiter.join(expected_values), authorized_obj_class=[list], none_checkable=True)

    def _check_obj_rule(self, obj : list) -> bool:
        return (obj is not None) & (all([expected_value in obj for expected_value in self.expected_values]))
    
class IntInRangeCheck(StdSimpleCheckRule):
    def __init__(self, name: str = 'Integer in range', range_min : int = 0, range_max : int = 1000000000
        , err_msg : str = f'Integer is not in the range') -> None:
        super().__init__(name=name, err_msg=err_msg, authorized_obj_class=[int], none_checkable=True)
        self.range_min = range_min
        self.range_max = range_max

    def _check_obj_rule(self, obj : int) -> bool:
        return (obj is not None) & (obj >= self.range_min) & (obj <= self.range_max)