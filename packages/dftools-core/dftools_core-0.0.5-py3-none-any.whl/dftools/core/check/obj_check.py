
from typing import List, Dict, TypeVar, Generic
from dftools.exceptions import MissingMandatoryArgumentException

from dftools.core.check.check_event import CheckEvent, CheckResult, CheckResults
from dftools.core.check.check_rule import CheckRule

T = TypeVar('T')

class ObjectCheckRule(Generic[T]) :
    """
        This is a checker interface to define specific object check rules, enabling the standard call to a check rule apply to a particular object.
        
        This checker contains : 
        - A check rule, a standard check rule
    """
    def __init__(self, rule : CheckRule) -> None:
        self.rule=rule

    def _check_obj_authorized(self, obj, expected_type : type) -> None:
        """
        Check that the object type is allowed, thus that the object provided is of the type T specific to this class.
        Raises an exception if any issue is encountered during the check
        
        Parameters
        -----------
            obj : the object to check
        """
        if obj is None:
            raise MissingMandatoryArgumentException(method_name='Check Object Authorized', object_type=type(self), argument_name='Object')
        #if type(obj) != expected_type:
        #    raise InvalidTypeArgumentException(method_name='Check Object Authorized', object_type=type(self), argument_name='Object', arg_expected_type=expected_type, arg_type=type(obj))
        return None
    
    def get_check_key(self, obj : T) -> str:
        raise NotImplementedError('The method get_check_key needs to be implemented')

    def get_object_to_check(self, obj : T):
        raise NotImplementedError('The method get_object_to_value needs to be implemented')

    def check(self, obj : T, root_key : str = None, parent_key : str = '') -> CheckEvent:
        """
        This method checks the object provided for the stored check rule and returns the Check Event.
        
        Parameters
        -----------
            obj : T
                The object to check

        Returns
        -----------
            The result CheckEvent of the CheckRule on the provided object
        """
        self._check_obj_authorized(obj, T)
        return self.rule.check(
            root_key=root_key
            , key=(parent_key if parent_key == '' else parent_key + '.') + self.get_check_key(obj)
            , obj=self.get_object_to_check(obj)
        )


class ObjectChecker(Generic[T]):
    def __init__(self) -> None:
        super().__init__()
    
    def check(self, obj : T) -> CheckResult:
        raise NotImplementedError('The method check needs to be implemented')
    
    def check_multiple(self, obj : List[T]) -> CheckResults:
        check_results = CheckResults()
        for obj_to_check in obj:
            check_results.append(self.check(obj_to_check))
        return check_results
    
class CheckerWrapper(Generic[T]):
    def __init__(self, obj_checkers : Dict[str, ObjectChecker]) -> None:
        self.obj_checkers = obj_checkers
    
    def get_checker_keys() -> List[str]:
        return list(self.obj_checkers.keys())
    
    def check(self, obj_dict : Dict[str, List[T]]) -> CheckResults:
        """
        Check that the object type is allowed, thus that the object provided is of the type T specific to this class.
        Raises an exception if any issue is encountered during the check
        
        Parameters
        -----------
            obj_dict : Dict[str, List[T]]
                The dictionnary of objects to be checked stored as list linked to a key, which is used to determine the Object Checker to use
        """
        if obj_dict is None :
            raise MissingMandatoryArgumentException(method_name='Check', object_type=type(self), argument_name='Object Dictionnary')
        if not all([key in list(self.obj_checkers.keys()) for key in list(obj_dict.keys())]):
            raise ValueError('The object dictionnary cannot be checked for all the keys : ' + ', '.join(list(obj_dict.keys())))
        check_results = CheckResults()
        for key, obj_list in obj_dict.items():
            check_results.extend(self.obj_checkers[key].check_multiple(obj_list))
        return check_results