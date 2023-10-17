#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .list import list as list_cls
from .list_properties import list_properties as list_properties_cls
from .duplicate import duplicate as duplicate_cls
from .display_frame import display_frame as display_frame_cls
from .hide_frame import hide_frame as hide_frame_cls
from .reference_frames_child import reference_frames_child

class reference_frames(NamedObject[reference_frames_child], _CreatableNamedObjectMixin[reference_frames_child]):
    """
    'reference_frames' child.
    """

    fluent_name = "reference-frames"

    command_names = \
        ['list', 'list_properties', 'duplicate', 'display_frame',
         'hide_frame']

    list: list_cls = list_cls
    """
    list command of reference_frames.
    """
    list_properties: list_properties_cls = list_properties_cls
    """
    list_properties command of reference_frames.
    """
    duplicate: duplicate_cls = duplicate_cls
    """
    duplicate command of reference_frames.
    """
    display_frame: display_frame_cls = display_frame_cls
    """
    display_frame command of reference_frames.
    """
    hide_frame: hide_frame_cls = hide_frame_cls
    """
    hide_frame command of reference_frames.
    """
    child_object_type: reference_frames_child = reference_frames_child
    """
    child_object_type of reference_frames.
    """
