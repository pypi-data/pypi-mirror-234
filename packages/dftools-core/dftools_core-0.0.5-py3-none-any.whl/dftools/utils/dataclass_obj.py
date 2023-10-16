import dataclasses
import copy

from dataclasses import dataclass

from dftools.utils.json_loadable import DfJsonLoadable

@dataclass
class DfClonable():
    
    @classmethod
    def deep_copy(cls, self):
        """
        Creates a deep copy of this object

        Returns
        -----------
            A new object cloned from this object instance
        """
        if isinstance(self, cls):
            return copy.deepcopy(self)
        return None


@dataclass
class DfDataClassObj(DfJsonLoadable, DfClonable):
    pass
