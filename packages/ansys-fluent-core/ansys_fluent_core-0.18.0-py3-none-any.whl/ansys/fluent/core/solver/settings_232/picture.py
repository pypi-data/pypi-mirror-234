#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .raytracer_image import raytracer_image as raytracer_image_cls
from .color_mode import color_mode as color_mode_cls
from .driver_options import driver_options as driver_options_cls
from .invert_background import invert_background as invert_background_cls
from .landscape import landscape as landscape_cls
from .x_resolution import x_resolution as x_resolution_cls
from .y_resolution import y_resolution as y_resolution_cls
from .dpi import dpi as dpi_cls
from .use_window_resolution import use_window_resolution as use_window_resolution_cls
from .standard_resolution import standard_resolution as standard_resolution_cls
from .jpeg_hardcopy_quality import jpeg_hardcopy_quality as jpeg_hardcopy_quality_cls
from .preview import preview as preview_cls
from .save_picture import save_picture as save_picture_cls
from .list_color_mode import list_color_mode as list_color_mode_cls
class picture(Group):
    """
    Enter the hardcopy/save-picture options menu.
    """

    fluent_name = "picture"

    child_names = \
        ['raytracer_image', 'color_mode', 'driver_options',
         'invert_background', 'landscape', 'x_resolution', 'y_resolution',
         'dpi', 'use_window_resolution', 'standard_resolution',
         'jpeg_hardcopy_quality']

    raytracer_image: raytracer_image_cls = raytracer_image_cls
    """
    raytracer_image child of picture.
    """
    color_mode: color_mode_cls = color_mode_cls
    """
    color_mode child of picture.
    """
    driver_options: driver_options_cls = driver_options_cls
    """
    driver_options child of picture.
    """
    invert_background: invert_background_cls = invert_background_cls
    """
    invert_background child of picture.
    """
    landscape: landscape_cls = landscape_cls
    """
    landscape child of picture.
    """
    x_resolution: x_resolution_cls = x_resolution_cls
    """
    x_resolution child of picture.
    """
    y_resolution: y_resolution_cls = y_resolution_cls
    """
    y_resolution child of picture.
    """
    dpi: dpi_cls = dpi_cls
    """
    dpi child of picture.
    """
    use_window_resolution: use_window_resolution_cls = use_window_resolution_cls
    """
    use_window_resolution child of picture.
    """
    standard_resolution: standard_resolution_cls = standard_resolution_cls
    """
    standard_resolution child of picture.
    """
    jpeg_hardcopy_quality: jpeg_hardcopy_quality_cls = jpeg_hardcopy_quality_cls
    """
    jpeg_hardcopy_quality child of picture.
    """
    command_names = \
        ['preview', 'save_picture', 'list_color_mode']

    preview: preview_cls = preview_cls
    """
    preview command of picture.
    """
    save_picture: save_picture_cls = save_picture_cls
    """
    save_picture command of picture.
    """
    list_color_mode: list_color_mode_cls = list_color_mode_cls
    """
    list_color_mode command of picture.
    """
