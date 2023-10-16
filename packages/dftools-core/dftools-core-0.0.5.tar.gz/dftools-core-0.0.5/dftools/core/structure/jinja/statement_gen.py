import os

from jinja2 import Template
from dataclasses import asdict

from dftools.events import log_event_default, StandardInfoEvent as StdInfoEvent
from dftools.core.structure import Structure, Namespace
"""
    Statement Generation methods
"""

def get_structure_jinja_dict(structure : Structure) -> dict:
    """
        Get a structure dictionnary for jinja rendering

    Parameters
    -----------
        structure : Structure
            A structure

    Returns
    -----------
        The structure dictionnary for jinja rendering
    """
    structure_dict = asdict(structure)
    structure_dict['tec_key'] = [tec_key_field.name for tec_key_field in structure.get_tec_key_fields()]
    structure_dict['func_key'] = [func_key_field.name for func_key_field in structure.get_func_key_fields()] \
        if len(structure.get_func_key_fields()) > 0 else structure_dict['tec_key']
    for field in structure_dict['fields']:
        field : dict
        characterisations = {}
        for characterisation in field['characterisations']:
            characterisations.update({characterisation['name'] : []})
        field.pop('characterisations')
        field.update({'characterisations' : characterisations})
    return structure_dict
    
def create_statement_on_same_structure(
        namespace : Namespace
        , structure :  Structure
        , non_reg_statement_template : Template) -> str:
    """Creates a statement based on a structure

    The template is rendered using the information :
    - structure : the structure

    Parameters
    ----------
    structure : Structure
        The namespace
    structure : Structure
        The structure 
    non_reg_statement_template : Template
        The template to use for statement rendering

    Returns
    ----------
    statement : str
        The statement rendered using the provided template with a single structure as parameter with its associated namespace
    """

    data_for_template = {
        "namespace" : asdict(namespace)
        , "structure" : get_structure_jinja_dict(structure)
    }

    statement = non_reg_statement_template.render(data_for_template)

    return statement
