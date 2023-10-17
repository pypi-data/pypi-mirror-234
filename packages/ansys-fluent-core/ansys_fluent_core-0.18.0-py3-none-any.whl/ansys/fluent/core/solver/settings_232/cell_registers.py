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
from .cell_registers_child import cell_registers_child

class cell_registers(NamedObject[cell_registers_child], _CreatableNamedObjectMixin[cell_registers_child]):
    """
    'cell_registers' child.
    """

    fluent_name = "cell-registers"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list_cls = list_cls
    """
    list command of cell_registers.
    """
    list_properties: list_properties_cls = list_properties_cls
    """
    list_properties command of cell_registers.
    """
    duplicate: duplicate_cls = duplicate_cls
    """
    duplicate command of cell_registers.
    """
    child_object_type: cell_registers_child = cell_registers_child
    """
    child_object_type of cell_registers.
    """
