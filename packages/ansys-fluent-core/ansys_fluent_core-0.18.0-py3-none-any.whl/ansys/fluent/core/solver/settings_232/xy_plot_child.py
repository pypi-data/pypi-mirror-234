#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .name_1 import name as name_cls
from .uid import uid as uid_cls
from .options_13 import options as options_cls
from .plot_direction import plot_direction as plot_direction_cls
from .x_axis_function import x_axis_function as x_axis_function_cls
from .y_axis_function import y_axis_function as y_axis_function_cls
from .surfaces_list import surfaces_list as surfaces_list_cls
from .physics_1 import physics as physics_cls
from .geometry_4 import geometry as geometry_cls
from .surfaces import surfaces as surfaces_cls
from .axes import axes as axes_cls
from .curves import curves as curves_cls
from .display_3 import display as display_cls
class xy_plot_child(Group):
    """
    'child_object_type' of xy_plot.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'uid', 'options', 'plot_direction', 'x_axis_function',
         'y_axis_function', 'surfaces_list', 'physics', 'geometry',
         'surfaces', 'axes', 'curves']

    name: name_cls = name_cls
    """
    name child of xy_plot_child.
    """
    uid: uid_cls = uid_cls
    """
    uid child of xy_plot_child.
    """
    options: options_cls = options_cls
    """
    options child of xy_plot_child.
    """
    plot_direction: plot_direction_cls = plot_direction_cls
    """
    plot_direction child of xy_plot_child.
    """
    x_axis_function: x_axis_function_cls = x_axis_function_cls
    """
    x_axis_function child of xy_plot_child.
    """
    y_axis_function: y_axis_function_cls = y_axis_function_cls
    """
    y_axis_function child of xy_plot_child.
    """
    surfaces_list: surfaces_list_cls = surfaces_list_cls
    """
    surfaces_list child of xy_plot_child.
    """
    physics: physics_cls = physics_cls
    """
    physics child of xy_plot_child.
    """
    geometry: geometry_cls = geometry_cls
    """
    geometry child of xy_plot_child.
    """
    surfaces: surfaces_cls = surfaces_cls
    """
    surfaces child of xy_plot_child.
    """
    axes: axes_cls = axes_cls
    """
    axes child of xy_plot_child.
    """
    curves: curves_cls = curves_cls
    """
    curves child of xy_plot_child.
    """
    command_names = \
        ['display']

    display: display_cls = display_cls
    """
    display command of xy_plot_child.
    """
