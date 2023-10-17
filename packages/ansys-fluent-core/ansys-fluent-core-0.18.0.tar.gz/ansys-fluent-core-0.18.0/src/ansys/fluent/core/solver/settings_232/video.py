#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .background_1 import background as background_cls
from .color_filter import color_filter as color_filter_cls
from .foreground_1 import foreground as foreground_cls
from .on import on as on_cls
from .pixel_size import pixel_size as pixel_size_cls
class video(Group):
    """
    Enter the video window options menu.
    """

    fluent_name = "video"

    child_names = \
        ['background', 'color_filter', 'foreground', 'on', 'pixel_size']

    background: background_cls = background_cls
    """
    background child of video.
    """
    color_filter: color_filter_cls = color_filter_cls
    """
    color_filter child of video.
    """
    foreground: foreground_cls = foreground_cls
    """
    foreground child of video.
    """
    on: on_cls = on_cls
    """
    on child of video.
    """
    pixel_size: pixel_size_cls = pixel_size_cls
    """
    pixel_size child of video.
    """
