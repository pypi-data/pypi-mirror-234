#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .axes_2 import axes as axes_cls
from .main import main as main_cls
from .scale_3 import scale as scale_cls
from .text import text as text_cls
from .video import video as video_cls
from .xy import xy as xy_cls
from .logo import logo as logo_cls
from .ruler_1 import ruler as ruler_cls
from .logo_color import logo_color as logo_color_cls
from .aspect_ratio import aspect_ratio as aspect_ratio_cls
class windows(Group):
    """
    'windows' child.
    """

    fluent_name = "windows"

    child_names = \
        ['axes', 'main', 'scale', 'text', 'video', 'xy', 'logo', 'ruler',
         'logo_color']

    axes: axes_cls = axes_cls
    """
    axes child of windows.
    """
    main: main_cls = main_cls
    """
    main child of windows.
    """
    scale: scale_cls = scale_cls
    """
    scale child of windows.
    """
    text: text_cls = text_cls
    """
    text child of windows.
    """
    video: video_cls = video_cls
    """
    video child of windows.
    """
    xy: xy_cls = xy_cls
    """
    xy child of windows.
    """
    logo: logo_cls = logo_cls
    """
    logo child of windows.
    """
    ruler: ruler_cls = ruler_cls
    """
    ruler child of windows.
    """
    logo_color: logo_color_cls = logo_color_cls
    """
    logo_color child of windows.
    """
    command_names = \
        ['aspect_ratio']

    aspect_ratio: aspect_ratio_cls = aspect_ratio_cls
    """
    aspect_ratio command of windows.
    """
