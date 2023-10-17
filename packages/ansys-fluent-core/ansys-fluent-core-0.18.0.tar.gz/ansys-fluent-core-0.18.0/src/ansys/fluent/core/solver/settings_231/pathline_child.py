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
from .options_6 import options as options_cls
from .range import range as range_cls
from .style_attribute import style_attribute as style_attribute_cls
from .accuracy_control_1 import accuracy_control as accuracy_control_cls
from .plot_1 import plot as plot_cls
from .step import step as step_cls
from .skip import skip as skip_cls
from .coarsen import coarsen as coarsen_cls
from .onzone import onzone as onzone_cls
from .onphysics import onphysics as onphysics_cls
from .field import field as field_cls
from .surfaces_list import surfaces_list as surfaces_list_cls
from .velocity_domain import velocity_domain as velocity_domain_cls
from .color_map import color_map as color_map_cls
from .draw_mesh import draw_mesh as draw_mesh_cls
from .mesh_object import mesh_object as mesh_object_cls
from .display_state_name import display_state_name as display_state_name_cls
from .physics import physics as physics_cls
from .geometry_3 import geometry as geometry_cls
from .surfaces import surfaces as surfaces_cls
from .axes import axes as axes_cls
from .curves import curves as curves_cls
from .display_2 import display as display_cls
class pathline_child(Group):
    """
    'child_object_type' of pathline.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'uid', 'options', 'range', 'style_attribute',
         'accuracy_control', 'plot', 'step', 'skip', 'coarsen', 'onzone',
         'onphysics', 'field', 'surfaces_list', 'velocity_domain',
         'color_map', 'draw_mesh', 'mesh_object', 'display_state_name',
         'physics', 'geometry', 'surfaces', 'axes', 'curves']

    name: name_cls = name_cls
    """
    name child of pathline_child.
    """
    uid: uid_cls = uid_cls
    """
    uid child of pathline_child.
    """
    options: options_cls = options_cls
    """
    options child of pathline_child.
    """
    range: range_cls = range_cls
    """
    range child of pathline_child.
    """
    style_attribute: style_attribute_cls = style_attribute_cls
    """
    style_attribute child of pathline_child.
    """
    accuracy_control: accuracy_control_cls = accuracy_control_cls
    """
    accuracy_control child of pathline_child.
    """
    plot: plot_cls = plot_cls
    """
    plot child of pathline_child.
    """
    step: step_cls = step_cls
    """
    step child of pathline_child.
    """
    skip: skip_cls = skip_cls
    """
    skip child of pathline_child.
    """
    coarsen: coarsen_cls = coarsen_cls
    """
    coarsen child of pathline_child.
    """
    onzone: onzone_cls = onzone_cls
    """
    onzone child of pathline_child.
    """
    onphysics: onphysics_cls = onphysics_cls
    """
    onphysics child of pathline_child.
    """
    field: field_cls = field_cls
    """
    field child of pathline_child.
    """
    surfaces_list: surfaces_list_cls = surfaces_list_cls
    """
    surfaces_list child of pathline_child.
    """
    velocity_domain: velocity_domain_cls = velocity_domain_cls
    """
    velocity_domain child of pathline_child.
    """
    color_map: color_map_cls = color_map_cls
    """
    color_map child of pathline_child.
    """
    draw_mesh: draw_mesh_cls = draw_mesh_cls
    """
    draw_mesh child of pathline_child.
    """
    mesh_object: mesh_object_cls = mesh_object_cls
    """
    mesh_object child of pathline_child.
    """
    display_state_name: display_state_name_cls = display_state_name_cls
    """
    display_state_name child of pathline_child.
    """
    physics: physics_cls = physics_cls
    """
    physics child of pathline_child.
    """
    geometry: geometry_cls = geometry_cls
    """
    geometry child of pathline_child.
    """
    surfaces: surfaces_cls = surfaces_cls
    """
    surfaces child of pathline_child.
    """
    axes: axes_cls = axes_cls
    """
    axes child of pathline_child.
    """
    curves: curves_cls = curves_cls
    """
    curves child of pathline_child.
    """
    command_names = \
        ['display']

    display: display_cls = display_cls
    """
    display command of pathline_child.
    """
