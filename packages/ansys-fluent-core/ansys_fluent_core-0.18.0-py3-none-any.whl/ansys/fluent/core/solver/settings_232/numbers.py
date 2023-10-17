#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .x_format import x_format as x_format_cls
from .x_axis_precision import x_axis_precision as x_axis_precision_cls
from .y_format import y_format as y_format_cls
from .y_axis_precision import y_axis_precision as y_axis_precision_cls
class numbers(Group):
    """
    'numbers' child.
    """

    fluent_name = "numbers"

    child_names = \
        ['x_format', 'x_axis_precision', 'y_format', 'y_axis_precision']

    x_format: x_format_cls = x_format_cls
    """
    x_format child of numbers.
    """
    x_axis_precision: x_axis_precision_cls = x_axis_precision_cls
    """
    x_axis_precision child of numbers.
    """
    y_format: y_format_cls = y_format_cls
    """
    y_format child of numbers.
    """
    y_axis_precision: y_axis_precision_cls = y_axis_precision_cls
    """
    y_axis_precision child of numbers.
    """
