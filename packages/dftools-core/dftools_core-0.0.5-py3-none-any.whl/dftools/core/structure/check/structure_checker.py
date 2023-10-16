
from typing import Dict, List

from dftools.core.check import CheckRule, CheckResult, ObjectCheckRule, ObjectChecker, CheckerWrapper
from dftools.core.structure.core import Structure, Field

class StructureCheckRule(ObjectCheckRule[Structure]):
    def __init__(self, rule: CheckRule) -> None:
        super().__init__(rule)
    
    def get_check_key(self, obj : Structure) -> str:
        return obj.name

    def get_object_to_check(self, obj : Structure):
        raise NotImplementedError('The method get_object_to_check needs to be implemented')


class FieldCheckRule(ObjectCheckRule[Field]):
    def __init__(self, rule: CheckRule) -> None:
        super().__init__(rule)
    
    def get_check_key(self, obj : Field) -> str:
        return obj.name

    def get_object_to_check(self, obj : Field):
        raise NotImplementedError('The method get_object_to_check needs to be implemented')

class StructureChecker(ObjectChecker[Structure]):
    def __init__(self
        , structure_check_rules : List[StructureCheckRule] = None
        , field_check_rules : List[FieldCheckRule]= None
        ) -> None:
        super().__init__()
        self.structure_check_rules = structure_check_rules if structure_check_rules is not None else []
        self.field_check_rules = field_check_rules if field_check_rules is not None else []
    
    def check(self, obj : Structure) -> CheckResult:
        check_events = CheckResult()
        for structure_check_rule in self.structure_check_rules:
            check_events.add_check(structure_check_rule.check(obj=obj))
        for field in obj.fields :
            for field_check_rule in self.field_check_rules:
                check_events.add_check(field_check_rule.check(field, root_key = obj.name, parent_key=obj.name + '.fields'))
        return check_events
    
class StructureCheckerWrapper(CheckerWrapper):
    def __init__(self, obj_checkers: Dict[str, ObjectChecker]) -> None:
        super().__init__(obj_checkers)