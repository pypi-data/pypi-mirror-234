#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .color_mode import color_mode as color_mode_cls
from .invert_background import invert_background as invert_background_cls
from .driver_options import driver_options as driver_options_cls
from .standard_resolution import standard_resolution as standard_resolution_cls
from .jpeg_hardcopy_quality import jpeg_hardcopy_quality as jpeg_hardcopy_quality_cls
from .landscape import landscape as landscape_cls
from .x_resolution import x_resolution as x_resolution_cls
from .y_resolution import y_resolution as y_resolution_cls
from .dpi import dpi as dpi_cls
from .use_window_resolution import use_window_resolution as use_window_resolution_cls
from .list_color_mode import list_color_mode as list_color_mode_cls
from .preview import preview as preview_cls
class picture_options(Group):
    """
    'picture_options' child.
    """

    fluent_name = "picture-options"

    child_names = \
        ['color_mode', 'invert_background', 'driver_options',
         'standard_resolution', 'jpeg_hardcopy_quality', 'landscape',
         'x_resolution', 'y_resolution', 'dpi', 'use_window_resolution']

    color_mode: color_mode_cls = color_mode_cls
    """
    color_mode child of picture_options.
    """
    invert_background: invert_background_cls = invert_background_cls
    """
    invert_background child of picture_options.
    """
    driver_options: driver_options_cls = driver_options_cls
    """
    driver_options child of picture_options.
    """
    standard_resolution: standard_resolution_cls = standard_resolution_cls
    """
    standard_resolution child of picture_options.
    """
    jpeg_hardcopy_quality: jpeg_hardcopy_quality_cls = jpeg_hardcopy_quality_cls
    """
    jpeg_hardcopy_quality child of picture_options.
    """
    landscape: landscape_cls = landscape_cls
    """
    landscape child of picture_options.
    """
    x_resolution: x_resolution_cls = x_resolution_cls
    """
    x_resolution child of picture_options.
    """
    y_resolution: y_resolution_cls = y_resolution_cls
    """
    y_resolution child of picture_options.
    """
    dpi: dpi_cls = dpi_cls
    """
    dpi child of picture_options.
    """
    use_window_resolution: use_window_resolution_cls = use_window_resolution_cls
    """
    use_window_resolution child of picture_options.
    """
    command_names = \
        ['list_color_mode', 'preview']

    list_color_mode: list_color_mode_cls = list_color_mode_cls
    """
    list_color_mode command of picture_options.
    """
    preview: preview_cls = preview_cls
    """
    preview command of picture_options.
    """
