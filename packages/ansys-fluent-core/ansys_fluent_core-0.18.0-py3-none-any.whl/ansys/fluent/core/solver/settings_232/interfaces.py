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
from .interfaces_child import interfaces_child

class interfaces(NamedObject[interfaces_child], _CreatableNamedObjectMixin[interfaces_child]):
    """
    'interfaces' child.
    """

    fluent_name = "interfaces"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list_cls = list_cls
    """
    list command of interfaces.
    """
    list_properties: list_properties_cls = list_properties_cls
    """
    list_properties command of interfaces.
    """
    duplicate: duplicate_cls = duplicate_cls
    """
    duplicate command of interfaces.
    """
    child_object_type: interfaces_child = interfaces_child
    """
    child_object_type of interfaces.
    """
