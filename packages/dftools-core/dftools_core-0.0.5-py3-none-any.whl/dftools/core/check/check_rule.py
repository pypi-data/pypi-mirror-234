
from dftools.core.check.check_event import CheckInfo, ErrorCheckInfo, CheckEvent

class CheckRule():
    """
        A check rule provides a standard method to validate a specific type of object.

        A check rule is valid for a list of object types, most commonly only one. 
        The authorized object classes are stored in the authorized_obj_class attribute

        Check general rules : 
        - none_checkable : bool
            True means that the object to check can be None
            False means that the object to check cannot be None thus rule returns an error 
            by default if provided object is None (default is False)
    """
    def __init__(self
        , name : str
        , authorized_obj_class : list
        , none_checkable : bool = False
        ) -> None:
        self.name = name
        self.authorized_obj_class = authorized_obj_class
        self.none_checkable = none_checkable

    def _check_obj_authorized(self, obj) -> CheckInfo:
        """
        Check that the object type is allowed.
        If the object is not authorized, a check info in error will be returned.

        Object is not authorized in the cases : 
        - If none_checkable is set to False for this check rule and if object is None, then an error is returned
        - If the object type is not part of the authorized object classes
        
        Parameters
        -----------
            obj : the object to check

        Returns
        -----------
            An error check info with the default error message, if the object is not authorized.
            None if object is authorized
        """
        if obj is None:
            if self.none_checkable is False:
                return ErrorCheckInfo('None cannot be checked')
            else:
                return None
        if type(obj) not in self.authorized_obj_class:
            return ErrorCheckInfo(str(type(obj)) + ' is not a valid type for rule : ' + self.name)
        return None

    def _check_obj(self, obj) -> CheckInfo:
        """
        This is the check rule to be applied on the object.
        
        This method should be overriden by the child class.

        Parameters
        -----------
            obj : the object to check

        Returns
        -----------
            The result of the check, as a CheckInfo object
        """
        raise NotImplementedError('The method _check_obj needs to be implemented')

    def _check(self, obj) -> CheckInfo:
        """
        This is the check method to be called to check an object.

        First, a check is done to verify that the object is authorized for this check.
        Secondly, if the object is authorized, the check is applied

        Parameters
        -----------
            obj : the object to check

        Returns
        -----------
            The result of the check, as a CheckInfo object
        """
        return self._check_obj_authorized(obj) if self._check_obj_authorized(obj) is not None else self._check_obj(obj)

    def check(self, root_key : str, key: str, obj) -> CheckEvent:
        """
        This method returns a check event for this check rule applied to the provided object.

        Parameters
        -----------
            key : the key for this check
            obj : the object to check

        Returns
        -----------
            The result of the check, as a CheckInfo object
        """
        check_obj=self._check(obj)
        return CheckEvent(
            rule_name=self.name
            , root_key=root_key if root_key is not None else key
            , key=key
            , status=check_obj.status
            , desc=check_obj.desc)

class SimpleCheckRule(CheckRule):
    """
        A simple check rule provides a standard method to validate a specific type of object.

        A check rule is valid for a list of object types, most commonly only one. 
        The authorized object classes are stored in the authorized_obj_class attribute

        Check general rules : 
        - none_checkable / 
            True means that the object to check can be None
            False means that the object to check cannot be None thus rule returns an error by default if provided object is None (default is False)
        - result_to_status / 
            Dictionnary providing standard check infos to apply to check result
    """
    def __init__(self
        , name : str
        , authorized_obj_class : list
        , result_to_status : dict
        , none_checkable : bool = False
        ) -> None:
        super().__init__(
            name=name
            , authorized_obj_class=authorized_obj_class
            , none_checkable=none_checkable
            )
        self.result_to_status = result_to_status

    def _check_obj_rule(self, obj) -> bool:
        """
        This is the check rule standard method to be applied on the object, which should return True or False.
        True when check is valid, False when check is not valid.

        This method should be overriden by child classes.
        
        Parameters
        -----------
            obj : the object to check

        Returns
        -----------
            True, when check is valid.
            False, when check is not valid
        """
        raise NotImplementedError('The method _check_obj_rule needs to be implemented')
   
    def _check_obj(self, obj) -> CheckInfo:
        """
        This is the check rule standard method to be applied on the object.
        
        This method uses the _check_obj_rule to get a standard result (VALID or ERROR).
        And based on this standard result, creates a check info based on this object result_to_status dictionnary.

        Parameters
        -----------
            obj : the object to check

        Returns
        -----------
            The result of the check, as a CheckInfo object
        """
        check_info_desc : dict = self.result_to_status[self._check_obj_rule(obj)]
        status = check_info_desc['status']
        desc = check_info_desc['desc'] if 'desc' in check_info_desc.keys() else None
        return CheckInfo(status=status, desc=desc)

class StdSimpleCheckRule(SimpleCheckRule):
    def __init__(self
        , name: str
        , err_msg : str
        , authorized_obj_class : list
        , none_checkable : bool = False) -> None:
        super().__init__(
            name=name
            , authorized_obj_class=authorized_obj_class
            , none_checkable=none_checkable
            , result_to_status={
                True : {"status": CheckInfo.VALID}
                , False : {"status" : CheckInfo.ERROR, "desc": err_msg}
            }
        )
class StdSimpleWarnCheckRule(SimpleCheckRule):
    def __init__(self
        , name: str
        , err_msg : str
        , authorized_obj_class : list
        , none_checkable : bool = False) -> None:
        super().__init__(
            name=name
            , authorized_obj_class=authorized_obj_class
            , none_checkable=none_checkable
            , result_to_status={
                True : {"status": CheckInfo.VALID}
                , False : {"status" : CheckInfo.WARN, "desc": err_msg}
            }
        )