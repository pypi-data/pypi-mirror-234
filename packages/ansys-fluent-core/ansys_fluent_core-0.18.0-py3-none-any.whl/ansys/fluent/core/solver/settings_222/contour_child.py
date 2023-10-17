#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .name import name as name_cls
from .field import field as field_cls
from .filled import filled as filled_cls
from .boundary_values import boundary_values as boundary_values_cls
from .contour_lines import contour_lines as contour_lines_cls
from .node_values import node_values as node_values_cls
from .surfaces_list import surfaces_list as surfaces_list_cls
from .range_option import range_option as range_option_cls
from .coloring_1 import coloring as coloring_cls
from .color_map import color_map as color_map_cls
from .draw_mesh import draw_mesh as draw_mesh_cls
from .mesh_object import mesh_object as mesh_object_cls
from .display_state_name import display_state_name as display_state_name_cls
from .physics import physics as physics_cls
from .geometry_1 import geometry as geometry_cls
from .surfaces import surfaces as surfaces_cls
from .display_1 import display as display_cls
class contour_child(Group):
    """
    'child_object_type' of contour.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'field', 'filled', 'boundary_values', 'contour_lines',
         'node_values', 'surfaces_list', 'range_option', 'coloring',
         'color_map', 'draw_mesh', 'mesh_object', 'display_state_name',
         'physics', 'geometry', 'surfaces']

    name: name_cls = name_cls
    """
    name child of contour_child.
    """
    field: field_cls = field_cls
    """
    field child of contour_child.
    """
    filled: filled_cls = filled_cls
    """
    filled child of contour_child.
    """
    boundary_values: boundary_values_cls = boundary_values_cls
    """
    boundary_values child of contour_child.
    """
    contour_lines: contour_lines_cls = contour_lines_cls
    """
    contour_lines child of contour_child.
    """
    node_values: node_values_cls = node_values_cls
    """
    node_values child of contour_child.
    """
    surfaces_list: surfaces_list_cls = surfaces_list_cls
    """
    surfaces_list child of contour_child.
    """
    range_option: range_option_cls = range_option_cls
    """
    range_option child of contour_child.
    """
    coloring: coloring_cls = coloring_cls
    """
    coloring child of contour_child.
    """
    color_map: color_map_cls = color_map_cls
    """
    color_map child of contour_child.
    """
    draw_mesh: draw_mesh_cls = draw_mesh_cls
    """
    draw_mesh child of contour_child.
    """
    mesh_object: mesh_object_cls = mesh_object_cls
    """
    mesh_object child of contour_child.
    """
    display_state_name: display_state_name_cls = display_state_name_cls
    """
    display_state_name child of contour_child.
    """
    physics: physics_cls = physics_cls
    """
    physics child of contour_child.
    """
    geometry: geometry_cls = geometry_cls
    """
    geometry child of contour_child.
    """
    surfaces: surfaces_cls = surfaces_cls
    """
    surfaces child of contour_child.
    """
    command_names = \
        ['display']

    display: display_cls = display_cls
    """
    display command of contour_child.
    """
