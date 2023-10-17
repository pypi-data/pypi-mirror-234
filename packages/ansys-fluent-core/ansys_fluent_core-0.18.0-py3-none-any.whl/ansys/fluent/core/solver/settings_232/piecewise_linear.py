#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .list_properties_1 import list_properties as list_properties_cls
from .piecewise_linear_child import piecewise_linear_child

class piecewise_linear(ListObject[piecewise_linear_child]):
    """
    'piecewise_linear' child.
    """

    fluent_name = "piecewise-linear"

    command_names = \
        ['list_properties']

    list_properties: list_properties_cls = list_properties_cls
    """
    list_properties command of piecewise_linear.
    """
    child_object_type: piecewise_linear_child = piecewise_linear_child
    """
    child_object_type of piecewise_linear.
    """
