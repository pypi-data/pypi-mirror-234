#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .visible import visible as visible_cls
from .size import size as size_cls
from .color import color as color_cls
from .log_scale import log_scale as log_scale_cls
from .format import format as format_cls
from .user_skip import user_skip as user_skip_cls
from .show_all import show_all as show_all_cls
from .position import position as position_cls
from .font_name import font_name as font_name_cls
from .font_automatic import font_automatic as font_automatic_cls
from .font_size import font_size as font_size_cls
from .length_1 import length as length_cls
from .width import width as width_cls
from .bground_transparent import bground_transparent as bground_transparent_cls
from .bground_color import bground_color as bground_color_cls
from .title_elements import title_elements as title_elements_cls
class color_map(Group):
    """
    'color_map' child.
    """

    fluent_name = "color-map"

    child_names = \
        ['visible', 'size', 'color', 'log_scale', 'format', 'user_skip',
         'show_all', 'position', 'font_name', 'font_automatic', 'font_size',
         'length', 'width', 'bground_transparent', 'bground_color',
         'title_elements']

    visible: visible_cls = visible_cls
    """
    visible child of color_map.
    """
    size: size_cls = size_cls
    """
    size child of color_map.
    """
    color: color_cls = color_cls
    """
    color child of color_map.
    """
    log_scale: log_scale_cls = log_scale_cls
    """
    log_scale child of color_map.
    """
    format: format_cls = format_cls
    """
    format child of color_map.
    """
    user_skip: user_skip_cls = user_skip_cls
    """
    user_skip child of color_map.
    """
    show_all: show_all_cls = show_all_cls
    """
    show_all child of color_map.
    """
    position: position_cls = position_cls
    """
    position child of color_map.
    """
    font_name: font_name_cls = font_name_cls
    """
    font_name child of color_map.
    """
    font_automatic: font_automatic_cls = font_automatic_cls
    """
    font_automatic child of color_map.
    """
    font_size: font_size_cls = font_size_cls
    """
    font_size child of color_map.
    """
    length: length_cls = length_cls
    """
    length child of color_map.
    """
    width: width_cls = width_cls
    """
    width child of color_map.
    """
    bground_transparent: bground_transparent_cls = bground_transparent_cls
    """
    bground_transparent child of color_map.
    """
    bground_color: bground_color_cls = bground_color_cls
    """
    bground_color child of color_map.
    """
    title_elements: title_elements_cls = title_elements_cls
    """
    title_elements child of color_map.
    """
