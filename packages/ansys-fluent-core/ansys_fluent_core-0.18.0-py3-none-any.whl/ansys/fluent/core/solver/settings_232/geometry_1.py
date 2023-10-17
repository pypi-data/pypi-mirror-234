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
from .geometry_child import geometry_child

class geometry(NamedObject[geometry_child], _CreatableNamedObjectMixin[geometry_child]):
    """
    Main menu to define a disk-section:
    
     - delete : delete a disk-section% - edit   : edit a disk-section
     - new    : create a new disk-section
     - rename : rename a vbm disk-section.
    
    """

    fluent_name = "geometry"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list_cls = list_cls
    """
    list command of geometry.
    """
    list_properties: list_properties_cls = list_properties_cls
    """
    list_properties command of geometry.
    """
    duplicate: duplicate_cls = duplicate_cls
    """
    duplicate command of geometry.
    """
    child_object_type: geometry_child = geometry_child
    """
    child_object_type of geometry.
    """
