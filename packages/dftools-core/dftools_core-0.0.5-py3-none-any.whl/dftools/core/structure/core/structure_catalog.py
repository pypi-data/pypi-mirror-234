from dataclasses import dataclass, field
from typing import List, Dict

from dftools.core.structure.core.structure import Structure
from dftools.core.structure.core.namespace import Namespace


@dataclass
class StructureCatalog():
    
    structures : Dict[Namespace, Dict[str, Structure]] = field(default_factory=dict)

    # Namespace methods
    def add_namespace(self, namespace : Namespace) -> None:
        if not(self.has_namespace(namespace)):
            self.structures.update({namespace : {}})

    def has_namespace(self, namespace : Namespace) -> bool:
        return namespace in self.structures.keys()
    
    def get_namespaces(self) -> List[Namespace]:
        return list(self.structures.keys())
    
    # Structure methods
    def has_structure(self, namespace: Namespace, name : str) -> bool:
        if namespace is None :
            raise ValueError('Namespace is mandatory for structure search in catalog')
        if name is None :
            raise ValueError('Structure Name is mandatory for structure search in catalog')
        return name in self.get_structures(namespace).keys()

    def get_structures(self, namespace : Namespace) -> Dict[str, Structure]:
        if self.has_namespace(namespace):
            return self.structures[namespace]
        raise ValueError('No Namespace available in the structure catalog for ' + namespace.__str__)

    def get_structure(self, namespace : Namespace, name : str) -> Structure:
        if self.has_structure(namespace, name):
            return self.structures[namespace][name]
        raise ValueError('No Structure available in the structure catalog for namespace : ' + namespace.__str__ \
                        + ' and structure name : ' + name)

    def get_structure_by_name(self, name : str) -> Structure:
        for namespace in self.get_namespaces():
            if self.has_structure(namespace, name):
                return self.structures[namespace][name]
        raise ValueError('No Structure available in the structure catalog with name : ' + name)

    def add_structure(self, namespace : Namespace, structure : Structure, prevent_namespace_creation : bool = False) -> None:
        if namespace is None :
            raise ValueError('Namespace is mandatory for structure addition in catalog')
        if structure is None :
            raise ValueError('Structure is mandatory for structure addition in catalog')
        if not(self.has_namespace(namespace)):
            if prevent_namespace_creation : 
                raise ValueError('No Namespace available in the structure catalog for ' + namespace.__str__)
            else :
                self.add_namespace(namespace)
        self.structures[namespace].update({structure.name : structure})    
