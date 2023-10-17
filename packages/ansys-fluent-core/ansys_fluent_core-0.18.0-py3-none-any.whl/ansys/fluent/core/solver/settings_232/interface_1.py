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
from .interface_child_1 import interface_child

class interface(NamedObject[interface_child], _CreatableNamedObjectMixin[interface_child]):
    """
    'interface' child.
    """

    fluent_name = "interface"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list_cls = list_cls
    """
    list command of interface.
    """
    list_properties: list_properties_cls = list_properties_cls
    """
    list_properties command of interface.
    """
    duplicate: duplicate_cls = duplicate_cls
    """
    duplicate command of interface.
    """
    child_object_type: interface_child = interface_child
    """
    child_object_type of interface.
    """
