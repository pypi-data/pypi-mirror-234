#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .fps import fps as fps_cls
from .format_2 import format as format_cls
from .quality_1 import quality as quality_cls
from .name_3 import name as name_cls
from .use_original_resolution import use_original_resolution as use_original_resolution_cls
from .scale_4 import scale as scale_cls
from .set_standard_resolution import set_standard_resolution as set_standard_resolution_cls
from .width_2 import width as width_cls
from .height_2 import height as height_cls
from .advance_quality import advance_quality as advance_quality_cls
class video(Group):
    """
    'video' child.
    """

    fluent_name = "video"

    child_names = \
        ['fps', 'format', 'quality', 'name', 'use_original_resolution',
         'scale', 'set_standard_resolution', 'width', 'height',
         'advance_quality']

    fps: fps_cls = fps_cls
    """
    fps child of video.
    """
    format: format_cls = format_cls
    """
    format child of video.
    """
    quality: quality_cls = quality_cls
    """
    quality child of video.
    """
    name: name_cls = name_cls
    """
    name child of video.
    """
    use_original_resolution: use_original_resolution_cls = use_original_resolution_cls
    """
    use_original_resolution child of video.
    """
    scale: scale_cls = scale_cls
    """
    scale child of video.
    """
    set_standard_resolution: set_standard_resolution_cls = set_standard_resolution_cls
    """
    set_standard_resolution child of video.
    """
    width: width_cls = width_cls
    """
    width child of video.
    """
    height: height_cls = height_cls
    """
    height child of video.
    """
    advance_quality: advance_quality_cls = advance_quality_cls
    """
    advance_quality child of video.
    """
