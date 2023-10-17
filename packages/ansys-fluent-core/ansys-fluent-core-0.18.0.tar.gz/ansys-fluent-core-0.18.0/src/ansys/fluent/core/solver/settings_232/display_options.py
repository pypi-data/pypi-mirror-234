#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .draw_mesh import draw_mesh as draw_mesh_cls
from .filled import filled as filled_cls
from .marker import marker as marker_cls
from .marker_symbol import marker_symbol as marker_symbol_cls
from .marker_size import marker_size as marker_size_cls
from .wireframe import wireframe as wireframe_cls
from .color import color as color_cls
class display_options(Group):
    """
    'display_options' child.
    """

    fluent_name = "display-options"

    child_names = \
        ['draw_mesh', 'filled', 'marker', 'marker_symbol', 'marker_size',
         'wireframe', 'color']

    draw_mesh: draw_mesh_cls = draw_mesh_cls
    """
    draw_mesh child of display_options.
    """
    filled: filled_cls = filled_cls
    """
    filled child of display_options.
    """
    marker: marker_cls = marker_cls
    """
    marker child of display_options.
    """
    marker_symbol: marker_symbol_cls = marker_symbol_cls
    """
    marker_symbol child of display_options.
    """
    marker_size: marker_size_cls = marker_size_cls
    """
    marker_size child of display_options.
    """
    wireframe: wireframe_cls = wireframe_cls
    """
    wireframe child of display_options.
    """
    color: color_cls = color_cls
    """
    color child of display_options.
    """
