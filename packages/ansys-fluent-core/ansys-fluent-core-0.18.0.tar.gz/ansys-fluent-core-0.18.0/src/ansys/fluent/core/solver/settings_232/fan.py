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
from .fan_child import fan_child

class fan(NamedObject[fan_child], _NonCreatableNamedObjectMixin[fan_child]):
    """
    'fan' child.
    """

    fluent_name = "fan"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list_cls = list_cls
    """
    list command of fan.
    """
    list_properties: list_properties_cls = list_properties_cls
    """
    list_properties command of fan.
    """
    duplicate: duplicate_cls = duplicate_cls
    """
    duplicate command of fan.
    """
    child_object_type: fan_child = fan_child
    """
    child_object_type of fan.
    """
