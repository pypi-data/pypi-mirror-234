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
from .porous_jump_child import porous_jump_child

class porous_jump(NamedObject[porous_jump_child], _NonCreatableNamedObjectMixin[porous_jump_child]):
    """
    'porous_jump' child.
    """

    fluent_name = "porous-jump"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list_cls = list_cls
    """
    list command of porous_jump.
    """
    list_properties: list_properties_cls = list_properties_cls
    """
    list_properties command of porous_jump.
    """
    duplicate: duplicate_cls = duplicate_cls
    """
    duplicate command of porous_jump.
    """
    child_object_type: porous_jump_child = porous_jump_child
    """
    child_object_type of porous_jump.
    """
