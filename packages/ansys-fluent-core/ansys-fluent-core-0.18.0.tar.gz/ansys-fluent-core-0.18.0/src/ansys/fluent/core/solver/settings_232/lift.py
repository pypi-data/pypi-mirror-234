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
from .force_child import force_child

class lift(NamedObject[force_child], _CreatableNamedObjectMixin[force_child]):
    """
    'lift' child.
    """

    fluent_name = "lift"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list_cls = list_cls
    """
    list command of lift.
    """
    list_properties: list_properties_cls = list_properties_cls
    """
    list_properties command of lift.
    """
    duplicate: duplicate_cls = duplicate_cls
    """
    duplicate command of lift.
    """
    child_object_type: force_child = force_child
    """
    child_object_type of lift.
    """
