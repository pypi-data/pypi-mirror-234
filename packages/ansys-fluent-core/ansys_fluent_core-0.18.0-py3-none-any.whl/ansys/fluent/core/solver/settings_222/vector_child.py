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
from .vector_field import vector_field as vector_field_cls
from .surfaces_list import surfaces_list as surfaces_list_cls
from .scale import scale as scale_cls
from .style import style as style_cls
from .skip import skip as skip_cls
from .vector_opt import vector_opt as vector_opt_cls
from .range_option import range_option as range_option_cls
from .color_map import color_map as color_map_cls
from .draw_mesh import draw_mesh as draw_mesh_cls
from .mesh_object import mesh_object as mesh_object_cls
from .display_state_name import display_state_name as display_state_name_cls
from .physics import physics as physics_cls
from .geometry_1 import geometry as geometry_cls
from .surfaces import surfaces as surfaces_cls
from .display_1 import display as display_cls
class vector_child(Group):
    """
    'child_object_type' of vector.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'field', 'vector_field', 'surfaces_list', 'scale', 'style',
         'skip', 'vector_opt', 'range_option', 'color_map', 'draw_mesh',
         'mesh_object', 'display_state_name', 'physics', 'geometry',
         'surfaces']

    name: name_cls = name_cls
    """
    name child of vector_child.
    """
    field: field_cls = field_cls
    """
    field child of vector_child.
    """
    vector_field: vector_field_cls = vector_field_cls
    """
    vector_field child of vector_child.
    """
    surfaces_list: surfaces_list_cls = surfaces_list_cls
    """
    surfaces_list child of vector_child.
    """
    scale: scale_cls = scale_cls
    """
    scale child of vector_child.
    """
    style: style_cls = style_cls
    """
    style child of vector_child.
    """
    skip: skip_cls = skip_cls
    """
    skip child of vector_child.
    """
    vector_opt: vector_opt_cls = vector_opt_cls
    """
    vector_opt child of vector_child.
    """
    range_option: range_option_cls = range_option_cls
    """
    range_option child of vector_child.
    """
    color_map: color_map_cls = color_map_cls
    """
    color_map child of vector_child.
    """
    draw_mesh: draw_mesh_cls = draw_mesh_cls
    """
    draw_mesh child of vector_child.
    """
    mesh_object: mesh_object_cls = mesh_object_cls
    """
    mesh_object child of vector_child.
    """
    display_state_name: display_state_name_cls = display_state_name_cls
    """
    display_state_name child of vector_child.
    """
    physics: physics_cls = physics_cls
    """
    physics child of vector_child.
    """
    geometry: geometry_cls = geometry_cls
    """
    geometry child of vector_child.
    """
    surfaces: surfaces_cls = surfaces_cls
    """
    surfaces child of vector_child.
    """
    command_names = \
        ['display']

    display: display_cls = display_cls
    """
    display command of vector_child.
    """
