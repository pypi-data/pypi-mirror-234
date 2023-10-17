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
from .options_7 import options as options_cls
from .filter_settings import filter_settings as filter_settings_cls
from .range import range as range_cls
from .style_attribute_1 import style_attribute as style_attribute_cls
from .vector_settings import vector_settings as vector_settings_cls
from .plot_1 import plot as plot_cls
from .track_single_particle_stream import track_single_particle_stream as track_single_particle_stream_cls
from .skip import skip as skip_cls
from .coarsen import coarsen as coarsen_cls
from .field import field as field_cls
from .injections_list import injections_list as injections_list_cls
from .free_stream_particles import free_stream_particles as free_stream_particles_cls
from .wall_film_particles import wall_film_particles as wall_film_particles_cls
from .track_pdf_particles import track_pdf_particles as track_pdf_particles_cls
from .color_map import color_map as color_map_cls
from .draw_mesh import draw_mesh as draw_mesh_cls
from .mesh_object import mesh_object as mesh_object_cls
from .display_state_name import display_state_name as display_state_name_cls
from .axes import axes as axes_cls
from .curves import curves as curves_cls
from .display_2 import display as display_cls
class particle_track_child(Group):
    """
    'child_object_type' of particle_track.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'uid', 'options', 'filter_settings', 'range',
         'style_attribute', 'vector_settings', 'plot',
         'track_single_particle_stream', 'skip', 'coarsen', 'field',
         'injections_list', 'free_stream_particles', 'wall_film_particles',
         'track_pdf_particles', 'color_map', 'draw_mesh', 'mesh_object',
         'display_state_name', 'axes', 'curves']

    name: name_cls = name_cls
    """
    name child of particle_track_child.
    """
    uid: uid_cls = uid_cls
    """
    uid child of particle_track_child.
    """
    options: options_cls = options_cls
    """
    options child of particle_track_child.
    """
    filter_settings: filter_settings_cls = filter_settings_cls
    """
    filter_settings child of particle_track_child.
    """
    range: range_cls = range_cls
    """
    range child of particle_track_child.
    """
    style_attribute: style_attribute_cls = style_attribute_cls
    """
    style_attribute child of particle_track_child.
    """
    vector_settings: vector_settings_cls = vector_settings_cls
    """
    vector_settings child of particle_track_child.
    """
    plot: plot_cls = plot_cls
    """
    plot child of particle_track_child.
    """
    track_single_particle_stream: track_single_particle_stream_cls = track_single_particle_stream_cls
    """
    track_single_particle_stream child of particle_track_child.
    """
    skip: skip_cls = skip_cls
    """
    skip child of particle_track_child.
    """
    coarsen: coarsen_cls = coarsen_cls
    """
    coarsen child of particle_track_child.
    """
    field: field_cls = field_cls
    """
    field child of particle_track_child.
    """
    injections_list: injections_list_cls = injections_list_cls
    """
    injections_list child of particle_track_child.
    """
    free_stream_particles: free_stream_particles_cls = free_stream_particles_cls
    """
    free_stream_particles child of particle_track_child.
    """
    wall_film_particles: wall_film_particles_cls = wall_film_particles_cls
    """
    wall_film_particles child of particle_track_child.
    """
    track_pdf_particles: track_pdf_particles_cls = track_pdf_particles_cls
    """
    track_pdf_particles child of particle_track_child.
    """
    color_map: color_map_cls = color_map_cls
    """
    color_map child of particle_track_child.
    """
    draw_mesh: draw_mesh_cls = draw_mesh_cls
    """
    draw_mesh child of particle_track_child.
    """
    mesh_object: mesh_object_cls = mesh_object_cls
    """
    mesh_object child of particle_track_child.
    """
    display_state_name: display_state_name_cls = display_state_name_cls
    """
    display_state_name child of particle_track_child.
    """
    axes: axes_cls = axes_cls
    """
    axes child of particle_track_child.
    """
    curves: curves_cls = curves_cls
    """
    curves child of particle_track_child.
    """
    command_names = \
        ['display']

    display: display_cls = display_cls
    """
    display command of particle_track_child.
    """
