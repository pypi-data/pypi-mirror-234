#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .list_2 import list as list_cls
from .list_properties_5 import list_properties as list_properties_cls
from .duplicate import duplicate as duplicate_cls
from .set_1 import set as set_cls
from .register_based_child import register_based_child

class register_based(NamedObject[register_based_child], _CreatableNamedObjectMixin[register_based_child]):
    """
    Set up the application of poor mesh numerics to cells in a register.
    """

    fluent_name = "register-based"

    command_names = \
        ['list', 'list_properties', 'duplicate', 'set']

    list: list_cls = list_cls
    """
    list command of register_based.
    """
    list_properties: list_properties_cls = list_properties_cls
    """
    list_properties command of register_based.
    """
    duplicate: duplicate_cls = duplicate_cls
    """
    duplicate command of register_based.
    """
    set: set_cls = set_cls
    """
    set command of register_based.
    """
    child_object_type: register_based_child = register_based_child
    """
    child_object_type of register_based.
    """
