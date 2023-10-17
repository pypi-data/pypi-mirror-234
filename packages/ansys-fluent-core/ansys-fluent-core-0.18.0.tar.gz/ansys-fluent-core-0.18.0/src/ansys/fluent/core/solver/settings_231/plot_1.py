#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .x_axis_function import x_axis_function as x_axis_function_cls
from .enabled_2 import enabled as enabled_cls
class plot(Group):
    """
    'plot' child.
    """

    fluent_name = "plot"

    child_names = \
        ['x_axis_function', 'enabled']

    x_axis_function: x_axis_function_cls = x_axis_function_cls
    """
    x_axis_function child of plot.
    """
    enabled: enabled_cls = enabled_cls
    """
    enabled child of plot.
    """
