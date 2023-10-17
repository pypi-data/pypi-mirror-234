#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .node_values import node_values as node_values_cls
from .position_on_x_axis import position_on_x_axis as position_on_x_axis_cls
from .position_on_y_axis import position_on_y_axis as position_on_y_axis_cls
class options(Group):
    """
    'options' child.
    """

    fluent_name = "options"

    child_names = \
        ['node_values', 'position_on_x_axis', 'position_on_y_axis']

    node_values: node_values_cls = node_values_cls
    """
    node_values child of options.
    """
    position_on_x_axis: position_on_x_axis_cls = position_on_x_axis_cls
    """
    position_on_x_axis child of options.
    """
    position_on_y_axis: position_on_y_axis_cls = position_on_y_axis_cls
    """
    position_on_y_axis child of options.
    """
