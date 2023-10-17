#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .change_type import change_type as change_type_cls
from .axis_child import axis_child

class symmetry(NamedObject[axis_child], _CreatableNamedObjectMixin[axis_child]):
    """
    'symmetry' child.
    """

    fluent_name = "symmetry"

    command_names = \
        ['change_type']

    change_type: change_type_cls = change_type_cls
    """
    change_type command of symmetry.
    """
    child_object_type: axis_child = axis_child
    """
    child_object_type of symmetry.
    """
