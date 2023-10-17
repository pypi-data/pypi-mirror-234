#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .name_1 import name as name_cls
from .field import field as field_cls
from .vector_field import vector_field as vector_field_cls
from .vector_phase import vector_phase as vector_phase_cls
from .surfaces_list import surfaces_list as surfaces_list_cls
from .surfaces import surfaces as surfaces_cls
from .lic_color_by_field import lic_color_by_field as lic_color_by_field_cls
from .lic_color import lic_color as lic_color_cls
from .lic_oriented import lic_oriented as lic_oriented_cls
from .lic_normalize import lic_normalize as lic_normalize_cls
from .lic_pixel_interpolation import lic_pixel_interpolation as lic_pixel_interpolation_cls
from .lic_max_steps import lic_max_steps as lic_max_steps_cls
from .texture_spacing import texture_spacing as texture_spacing_cls
from .texture_size import texture_size as texture_size_cls
from .lic_intensity_factor import lic_intensity_factor as lic_intensity_factor_cls
from .lic_image_filter import lic_image_filter as lic_image_filter_cls
from .lic_intensity_alpha import lic_intensity_alpha as lic_intensity_alpha_cls
from .lic_fast import lic_fast as lic_fast_cls
from .gray_scale import gray_scale as gray_scale_cls
from .image_to_display import image_to_display as image_to_display_cls
from .range_option import range_option as range_option_cls
from .color_map import color_map as color_map_cls
from .draw_mesh import draw_mesh as draw_mesh_cls
from .mesh_object import mesh_object as mesh_object_cls
from .display_state_name import display_state_name as display_state_name_cls
from .display_3 import display as display_cls
from .update_min_max import update_min_max as update_min_max_cls
class lic_child(Group):
    """
    'child_object_type' of lic.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'field', 'vector_field', 'vector_phase', 'surfaces_list',
         'surfaces', 'lic_color_by_field', 'lic_color', 'lic_oriented',
         'lic_normalize', 'lic_pixel_interpolation', 'lic_max_steps',
         'texture_spacing', 'texture_size', 'lic_intensity_factor',
         'lic_image_filter', 'lic_intensity_alpha', 'lic_fast', 'gray_scale',
         'image_to_display', 'range_option', 'color_map', 'draw_mesh',
         'mesh_object', 'display_state_name']

    name: name_cls = name_cls
    """
    name child of lic_child.
    """
    field: field_cls = field_cls
    """
    field child of lic_child.
    """
    vector_field: vector_field_cls = vector_field_cls
    """
    vector_field child of lic_child.
    """
    vector_phase: vector_phase_cls = vector_phase_cls
    """
    vector_phase child of lic_child.
    """
    surfaces_list: surfaces_list_cls = surfaces_list_cls
    """
    surfaces_list child of lic_child.
    """
    surfaces: surfaces_cls = surfaces_cls
    """
    surfaces child of lic_child.
    """
    lic_color_by_field: lic_color_by_field_cls = lic_color_by_field_cls
    """
    lic_color_by_field child of lic_child.
    """
    lic_color: lic_color_cls = lic_color_cls
    """
    lic_color child of lic_child.
    """
    lic_oriented: lic_oriented_cls = lic_oriented_cls
    """
    lic_oriented child of lic_child.
    """
    lic_normalize: lic_normalize_cls = lic_normalize_cls
    """
    lic_normalize child of lic_child.
    """
    lic_pixel_interpolation: lic_pixel_interpolation_cls = lic_pixel_interpolation_cls
    """
    lic_pixel_interpolation child of lic_child.
    """
    lic_max_steps: lic_max_steps_cls = lic_max_steps_cls
    """
    lic_max_steps child of lic_child.
    """
    texture_spacing: texture_spacing_cls = texture_spacing_cls
    """
    texture_spacing child of lic_child.
    """
    texture_size: texture_size_cls = texture_size_cls
    """
    texture_size child of lic_child.
    """
    lic_intensity_factor: lic_intensity_factor_cls = lic_intensity_factor_cls
    """
    lic_intensity_factor child of lic_child.
    """
    lic_image_filter: lic_image_filter_cls = lic_image_filter_cls
    """
    lic_image_filter child of lic_child.
    """
    lic_intensity_alpha: lic_intensity_alpha_cls = lic_intensity_alpha_cls
    """
    lic_intensity_alpha child of lic_child.
    """
    lic_fast: lic_fast_cls = lic_fast_cls
    """
    lic_fast child of lic_child.
    """
    gray_scale: gray_scale_cls = gray_scale_cls
    """
    gray_scale child of lic_child.
    """
    image_to_display: image_to_display_cls = image_to_display_cls
    """
    image_to_display child of lic_child.
    """
    range_option: range_option_cls = range_option_cls
    """
    range_option child of lic_child.
    """
    color_map: color_map_cls = color_map_cls
    """
    color_map child of lic_child.
    """
    draw_mesh: draw_mesh_cls = draw_mesh_cls
    """
    draw_mesh child of lic_child.
    """
    mesh_object: mesh_object_cls = mesh_object_cls
    """
    mesh_object child of lic_child.
    """
    display_state_name: display_state_name_cls = display_state_name_cls
    """
    display_state_name child of lic_child.
    """
    command_names = \
        ['display', 'update_min_max']

    display: display_cls = display_cls
    """
    display command of lic_child.
    """
    update_min_max: update_min_max_cls = update_min_max_cls
    """
    update_min_max command of lic_child.
    """
