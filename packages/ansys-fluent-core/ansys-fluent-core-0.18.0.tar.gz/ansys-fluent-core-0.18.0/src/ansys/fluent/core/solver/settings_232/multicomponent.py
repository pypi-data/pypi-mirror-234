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
from .multicomponent_child import multicomponent_child

class multicomponent(NamedObject[multicomponent_child], _NonCreatableNamedObjectMixin[multicomponent_child]):
    """
    'multicomponent' child.
    """

    fluent_name = "multicomponent"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list_cls = list_cls
    """
    list command of multicomponent.
    """
    list_properties: list_properties_cls = list_properties_cls
    """
    list_properties command of multicomponent.
    """
    duplicate: duplicate_cls = duplicate_cls
    """
    duplicate command of multicomponent.
    """
    child_object_type: multicomponent_child = multicomponent_child
    """
    child_object_type of multicomponent.
    """
