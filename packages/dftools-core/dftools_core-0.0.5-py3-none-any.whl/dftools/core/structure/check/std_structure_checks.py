
from dftools.core.check import StringValuedCheck, ListIsNotEmptyCheck, ListIsNotEmptyWarnCheck, ListContainsMandatoryValuesCheck, CheckRule
from dftools.core.structure.check.structure_checker import StructureCheckRule, FieldCheckRule
from dftools.core.structure.core import Structure, Field

class StructureCheckRuleCommentFilled(StructureCheckRule):
    def __init__(self) -> None:
        super().__init__(StringValuedCheck(name = 'Structure comment filled', err_msg='Structure comment is not filled'))
    
    def get_object_to_check(self, obj : Structure):
        return obj.desc
    
class StructureCheckRuleFieldPresent(StructureCheckRule):
    def __init__(self) -> None:
        super().__init__(ListIsNotEmptyCheck(name = 'Structure contains fields', err_msg='Structure should contain fields'))
    
    def get_object_to_check(self, obj : Structure):
        return obj.fields
    
class StructureCheckRuleOnName(StructureCheckRule):
    def __init__(self, check_rule : CheckRule) -> None:
        super().__init__(check_rule)
    
    def get_object_to_check(self, obj : Structure):
        return obj.name

class StructureCheckRulePrimaryKeyPresent(StructureCheckRule):
    def __init__(self) -> None:
        super().__init__(ListIsNotEmptyWarnCheck(name = 'Structure contains primary key', err_msg='Structure might require a primary key'))
    
    def get_object_to_check(self, obj : Structure):
        return obj.get_tec_key_fields()

class StructureCheckRuleMandatoryFields(StructureCheckRule):
    def __init__(self, expected_values : list) -> None:
        super().__init__(ListContainsMandatoryValuesCheck(name = 'Structure contains mandatory fields', err_msg='Structure does not contain all the mandatory fields'
            , expected_values=expected_values, err_value_delimiter = ', ')
        )
    
    def get_object_to_check(self, obj : Structure):
        return obj.get_field_names()



class FieldCheckRuleCommentFilled(FieldCheckRule):
    def __init__(self) -> None:
        super().__init__(StringValuedCheck(name = 'Field comment filled', err_msg='Field comment is not filled'))
    
    def get_object_to_check(self, obj : Field):
        return obj.desc

class FieldCheckRuleOnLength(FieldCheckRule):
    def __init__(self, check_rule : CheckRule) -> None:
        super().__init__(check_rule)
    
    def get_object_to_check(self, obj : Field):
        return obj.length