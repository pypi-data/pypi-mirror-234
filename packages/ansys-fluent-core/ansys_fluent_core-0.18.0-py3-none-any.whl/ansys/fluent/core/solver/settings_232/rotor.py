#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .list import list as list_cls
from .list_properties import list_properties as list_properties_cls
from .duplicate import duplicate as duplicate_cls
from .rotor_child import rotor_child

class rotor(NamedObject[rotor_child], _CreatableNamedObjectMixin[rotor_child]):
    """
    Main menu to define a rotor disk:
    
     - delete : delete a vbm disk
     - edit   : edit a vbm disk
     - new    : create a new vbm disk
     - rename : rename a vbm disk.
    
    """

    fluent_name = "rotor"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list_cls = list_cls
    """
    list command of rotor.
    """
    list_properties: list_properties_cls = list_properties_cls
    """
    list_properties command of rotor.
    """
    duplicate: duplicate_cls = duplicate_cls
    """
    duplicate command of rotor.
    """
    child_object_type: rotor_child = rotor_child
    """
    child_object_type of rotor.
    """
