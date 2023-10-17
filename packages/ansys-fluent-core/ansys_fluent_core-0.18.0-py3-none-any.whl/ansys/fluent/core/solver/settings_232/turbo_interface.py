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
from .turbo_interface_child import turbo_interface_child

class turbo_interface(NamedObject[turbo_interface_child], _CreatableNamedObjectMixin[turbo_interface_child]):
    """
    'turbo_interface' child.
    """

    fluent_name = "turbo-interface"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list_cls = list_cls
    """
    list command of turbo_interface.
    """
    list_properties: list_properties_cls = list_properties_cls
    """
    list_properties command of turbo_interface.
    """
    duplicate: duplicate_cls = duplicate_cls
    """
    duplicate command of turbo_interface.
    """
    child_object_type: turbo_interface_child = turbo_interface_child
    """
    child_object_type of turbo_interface.
    """
