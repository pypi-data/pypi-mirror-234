#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .auto_scale_2 import auto_scale as auto_scale_cls
from .clip_to_range_2 import clip_to_range as clip_to_range_cls
from .surfaces_1 import surfaces as surfaces_cls
from .filled_contours import filled_contours as filled_contours_cls
from .global_range_1 import global_range as global_range_cls
from .line_contours import line_contours as line_contours_cls
from .log_scale_2 import log_scale as log_scale_cls
from .n_contour import n_contour as n_contour_cls
from .node_values_2 import node_values as node_values_cls
from .render_mesh import render_mesh as render_mesh_cls
from .coloring_2 import coloring as coloring_cls
class contours(Group):
    """
    'contours' child.
    """

    fluent_name = "contours"

    child_names = \
        ['auto_scale', 'clip_to_range', 'surfaces', 'filled_contours',
         'global_range', 'line_contours', 'log_scale', 'n_contour',
         'node_values', 'render_mesh', 'coloring']

    auto_scale: auto_scale_cls = auto_scale_cls
    """
    auto_scale child of contours.
    """
    clip_to_range: clip_to_range_cls = clip_to_range_cls
    """
    clip_to_range child of contours.
    """
    surfaces: surfaces_cls = surfaces_cls
    """
    surfaces child of contours.
    """
    filled_contours: filled_contours_cls = filled_contours_cls
    """
    filled_contours child of contours.
    """
    global_range: global_range_cls = global_range_cls
    """
    global_range child of contours.
    """
    line_contours: line_contours_cls = line_contours_cls
    """
    line_contours child of contours.
    """
    log_scale: log_scale_cls = log_scale_cls
    """
    log_scale child of contours.
    """
    n_contour: n_contour_cls = n_contour_cls
    """
    n_contour child of contours.
    """
    node_values: node_values_cls = node_values_cls
    """
    node_values child of contours.
    """
    render_mesh: render_mesh_cls = render_mesh_cls
    """
    render_mesh child of contours.
    """
    coloring: coloring_cls = coloring_cls
    """
    coloring child of contours.
    """
