#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .x_axis_2 import x_axis as x_axis_cls
from .x_axis_min import x_axis_min as x_axis_min_cls
from .x_axis_max import x_axis_max as x_axis_max_cls
from .y_axis_2 import y_axis as y_axis_cls
from .y_axis_min import y_axis_min as y_axis_min_cls
from .y_axis_max import y_axis_max as y_axis_max_cls
class auto_scale(Group):
    """
    'auto_scale' child.
    """

    fluent_name = "auto-scale"

    child_names = \
        ['x_axis', 'x_axis_min', 'x_axis_max', 'y_axis', 'y_axis_min',
         'y_axis_max']

    x_axis: x_axis_cls = x_axis_cls
    """
    x_axis child of auto_scale.
    """
    x_axis_min: x_axis_min_cls = x_axis_min_cls
    """
    x_axis_min child of auto_scale.
    """
    x_axis_max: x_axis_max_cls = x_axis_max_cls
    """
    x_axis_max child of auto_scale.
    """
    y_axis: y_axis_cls = y_axis_cls
    """
    y_axis child of auto_scale.
    """
    y_axis_min: y_axis_min_cls = y_axis_min_cls
    """
    y_axis_min child of auto_scale.
    """
    y_axis_max: y_axis_max_cls = y_axis_max_cls
    """
    y_axis_max child of auto_scale.
    """
