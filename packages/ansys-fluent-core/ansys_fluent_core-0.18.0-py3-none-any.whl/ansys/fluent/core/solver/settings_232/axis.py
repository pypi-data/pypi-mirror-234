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
from .axis_child import axis_child

class axis(NamedObject[axis_child], _NonCreatableNamedObjectMixin[axis_child]):
    """
    'axis' child.
    """

    fluent_name = "axis"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list_cls = list_cls
    """
    list command of axis.
    """
    list_properties: list_properties_cls = list_properties_cls
    """
    list_properties command of axis.
    """
    duplicate: duplicate_cls = duplicate_cls
    """
    duplicate command of axis.
    """
    child_object_type: axis_child = axis_child
    """
    child_object_type of axis.
    """
