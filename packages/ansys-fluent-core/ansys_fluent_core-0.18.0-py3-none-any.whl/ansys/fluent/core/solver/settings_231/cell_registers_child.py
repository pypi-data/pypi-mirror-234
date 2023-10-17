#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .name_1 import name as name_cls
from .python_name import python_name as python_name_cls
from .type_2 import type as type_cls
from .display_options import display_options as display_options_cls
class cell_registers_child(Group):
    """
    'child_object_type' of cell_registers.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'python_name', 'type', 'display_options']

    name: name_cls = name_cls
    """
    name child of cell_registers_child.
    """
    python_name: python_name_cls = python_name_cls
    """
    python_name child of cell_registers_child.
    """
    type: type_cls = type_cls
    """
    type child of cell_registers_child.
    """
    display_options: display_options_cls = display_options_cls
    """
    display_options child of cell_registers_child.
    """
