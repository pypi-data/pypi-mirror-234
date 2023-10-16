
import logging
from typing import Any, List, Dict

from dftools.service.core.object_std_service import ObjReadHelper, ObjectStandardProviderService
from dftools.core.structure import StructureTemplate
from dftools.core.dataflow import DataFlowDefTemplate

class DfObjects():
    STRUCTURE_TEMPLATE = 'structure_template'
    DATA_FLOW_DEF_TEMPLATE = 'data_flow_def_template'

DF_READ_HELPER_OBJECTS : Dict[str, ObjReadHelper] = {
    DfObjects.STRUCTURE_TEMPLATE : 
        ObjReadHelper(DfObjects.STRUCTURE_TEMPLATE, True, DfObjects.STRUCTURE_TEMPLATE, None, StructureTemplate), 
    DfObjects.DATA_FLOW_DEF_TEMPLATE : 
        ObjReadHelper(DfObjects.DATA_FLOW_DEF_TEMPLATE, True, DfObjects.DATA_FLOW_DEF_TEMPLATE, None, DataFlowDefTemplate),
}

class DFObjProviderService(ObjectStandardProviderService):

    def __init__(self, system_folder : str, user_folder : str, object_read_helper_dict : Dict[str, ObjReadHelper] = DF_READ_HELPER_OBJECTS) -> None:
        self.logger = logging.getLogger(__name__)
        ObjectStandardProviderService.__init__(self, system_folder=system_folder, user_folder=user_folder, object_read_helper_dict=object_read_helper_dict)

    # Structure Template methods
    def get_structure_templates(self) -> Dict[str, StructureTemplate]:
        return self.get_dict(DfObjects.STRUCTURE_TEMPLATE)
    
    def get_structure_templates_by_name(self, object_keys : List[str]) -> List[StructureTemplate]:
        return self.get_objects(DfObjects.STRUCTURE_TEMPLATE, object_keys)
    
    def get_structure_templates_by_name_as_dict(self, object_keys : List[str]) -> Dict[str, StructureTemplate]:
        return self.get_objects_as_dict(DfObjects.STRUCTURE_TEMPLATE, object_keys)
    
    def get_structure_template(self, name : str) -> StructureTemplate:
        return self.get_object(DfObjects.STRUCTURE_TEMPLATE, name)
    
    # Data Flow Definition Template methods
    def get_data_flow_def_templates(self) -> Dict[str, DataFlowDefTemplate]:
        return self.get_dict(DfObjects.DATA_FLOW_DEF_TEMPLATE)
    
    def get_data_flow_def_templates_by_name(self, object_keys : List[str]) -> List[DataFlowDefTemplate]:
        return self.get_objects(DfObjects.DATA_FLOW_DEF_TEMPLATE, object_keys)
    
    def get_data_flow_def_templates_by_name_as_dict(self, object_keys : List[str]) -> Dict[str, DataFlowDefTemplate]:
        return self.get_objects_as_dict(DfObjects.DATA_FLOW_DEF_TEMPLATE, object_keys)
    
    def get_data_flow_def_template(self, name : str) -> DataFlowDefTemplate:
        return self.get_object(DfObjects.DATA_FLOW_DEF_TEMPLATE, name)
    