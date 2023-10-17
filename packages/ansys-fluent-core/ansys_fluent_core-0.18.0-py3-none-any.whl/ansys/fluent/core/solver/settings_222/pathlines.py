#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .display import display as display_cls
from .pathlines_child import pathlines_child

class pathlines(NamedObject[pathlines_child], _CreatableNamedObjectMixin[pathlines_child]):
    """
    'pathlines' child.
    """

    fluent_name = "pathlines"

    command_names = \
        ['display']

    display: display_cls = display_cls
    """
    display command of pathlines.
    """
    child_object_type: pathlines_child = pathlines_child
    """
    child_object_type of pathlines.
    """
