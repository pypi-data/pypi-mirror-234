#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .front_faces_transparent import front_faces_transparent as front_faces_transparent_cls
from .projection_1 import projection as projection_cls
from .axes_1 import axes as axes_cls
from .ruler import ruler as ruler_cls
from .title import title as title_cls
from .boundary_marker import boundary_marker as boundary_marker_cls
from .anti_aliasing import anti_aliasing as anti_aliasing_cls
from .reflections import reflections as reflections_cls
from .static_shadows import static_shadows as static_shadows_cls
from .dynamic_shadows import dynamic_shadows as dynamic_shadows_cls
from .grid_plane import grid_plane as grid_plane_cls
from .headlights import headlights as headlights_cls
from .lighting import lighting as lighting_cls
from .view_name import view_name as view_name_cls
class display_states_child(Group):
    """
    'child_object_type' of display_states.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['front_faces_transparent', 'projection', 'axes', 'ruler', 'title',
         'boundary_marker', 'anti_aliasing', 'reflections', 'static_shadows',
         'dynamic_shadows', 'grid_plane', 'headlights', 'lighting',
         'view_name']

    front_faces_transparent: front_faces_transparent_cls = front_faces_transparent_cls
    """
    front_faces_transparent child of display_states_child.
    """
    projection: projection_cls = projection_cls
    """
    projection child of display_states_child.
    """
    axes: axes_cls = axes_cls
    """
    axes child of display_states_child.
    """
    ruler: ruler_cls = ruler_cls
    """
    ruler child of display_states_child.
    """
    title: title_cls = title_cls
    """
    title child of display_states_child.
    """
    boundary_marker: boundary_marker_cls = boundary_marker_cls
    """
    boundary_marker child of display_states_child.
    """
    anti_aliasing: anti_aliasing_cls = anti_aliasing_cls
    """
    anti_aliasing child of display_states_child.
    """
    reflections: reflections_cls = reflections_cls
    """
    reflections child of display_states_child.
    """
    static_shadows: static_shadows_cls = static_shadows_cls
    """
    static_shadows child of display_states_child.
    """
    dynamic_shadows: dynamic_shadows_cls = dynamic_shadows_cls
    """
    dynamic_shadows child of display_states_child.
    """
    grid_plane: grid_plane_cls = grid_plane_cls
    """
    grid_plane child of display_states_child.
    """
    headlights: headlights_cls = headlights_cls
    """
    headlights child of display_states_child.
    """
    lighting: lighting_cls = lighting_cls
    """
    lighting child of display_states_child.
    """
    view_name: view_name_cls = view_name_cls
    """
    view_name child of display_states_child.
    """
