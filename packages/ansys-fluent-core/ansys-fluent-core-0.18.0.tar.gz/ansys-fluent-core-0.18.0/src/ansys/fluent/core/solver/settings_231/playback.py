#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .set_custom_frames import set_custom_frames as set_custom_frames_cls
from .video_1 import video as video_cls
from .read_animation import read_animation as read_animation_cls
from .write_animation import write_animation as write_animation_cls
from .stored_view import stored_view as stored_view_cls
class playback(Group):
    """
    'playback' child.
    """

    fluent_name = "playback"

    child_names = \
        ['set_custom_frames', 'video']

    set_custom_frames: set_custom_frames_cls = set_custom_frames_cls
    """
    set_custom_frames child of playback.
    """
    video: video_cls = video_cls
    """
    video child of playback.
    """
    command_names = \
        ['read_animation', 'write_animation', 'stored_view']

    read_animation: read_animation_cls = read_animation_cls
    """
    read_animation command of playback.
    """
    write_animation: write_animation_cls = write_animation_cls
    """
    write_animation command of playback.
    """
    stored_view: stored_view_cls = stored_view_cls
    """
    stored_view command of playback.
    """
