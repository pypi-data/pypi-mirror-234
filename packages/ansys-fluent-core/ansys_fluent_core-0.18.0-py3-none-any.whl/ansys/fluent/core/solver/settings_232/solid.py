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
from .solid_child import solid_child

class solid(NamedObject[solid_child], _CreatableNamedObjectMixin[solid_child]):
    """
    'solid' child.
    """

    fluent_name = "solid"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list_cls = list_cls
    """
    list command of solid.
    """
    list_properties: list_properties_cls = list_properties_cls
    """
    list_properties command of solid.
    """
    duplicate: duplicate_cls = duplicate_cls
    """
    duplicate command of solid.
    """
    child_object_type: solid_child = solid_child
    """
    child_object_type of solid.
    """
