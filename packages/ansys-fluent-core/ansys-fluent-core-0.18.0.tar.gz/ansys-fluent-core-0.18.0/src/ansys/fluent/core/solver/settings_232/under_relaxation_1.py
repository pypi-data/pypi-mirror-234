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
from .axis_direction_child import axis_direction_child

class under_relaxation(NamedObject[axis_direction_child], _NonCreatableNamedObjectMixin[axis_direction_child]):
    """
    Enter Under Relaxation Menu.
    """

    fluent_name = "under-relaxation"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list_cls = list_cls
    """
    list command of under_relaxation.
    """
    list_properties: list_properties_cls = list_properties_cls
    """
    list_properties command of under_relaxation.
    """
    duplicate: duplicate_cls = duplicate_cls
    """
    duplicate command of under_relaxation.
    """
    child_object_type: axis_direction_child = axis_direction_child
    """
    child_object_type of under_relaxation.
    """
