#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .name_1 import name as name_cls
from .title import title as title_cls
from .temporary import temporary as temporary_cls
from .graphics_objects import graphics_objects as graphics_objects_cls
from .display_state_name import display_state_name as display_state_name_cls
from .display_2 import display as display_cls
class scene_child(Group):
    """
    'child_object_type' of scene.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'title', 'temporary', 'graphics_objects',
         'display_state_name']

    name: name_cls = name_cls
    """
    name child of scene_child.
    """
    title: title_cls = title_cls
    """
    title child of scene_child.
    """
    temporary: temporary_cls = temporary_cls
    """
    temporary child of scene_child.
    """
    graphics_objects: graphics_objects_cls = graphics_objects_cls
    """
    graphics_objects child of scene_child.
    """
    display_state_name: display_state_name_cls = display_state_name_cls
    """
    display_state_name child of scene_child.
    """
    command_names = \
        ['display']

    display: display_cls = display_cls
    """
    display command of scene_child.
    """
