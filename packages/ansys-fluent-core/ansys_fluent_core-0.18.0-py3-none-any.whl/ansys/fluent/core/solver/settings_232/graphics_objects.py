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
from .graphics_objects_child import graphics_objects_child

class graphics_objects(NamedObject[graphics_objects_child], _CreatableNamedObjectMixin[graphics_objects_child]):
    """
    'graphics_objects' child.
    """

    fluent_name = "graphics-objects"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list_cls = list_cls
    """
    list command of graphics_objects.
    """
    list_properties: list_properties_cls = list_properties_cls
    """
    list_properties command of graphics_objects.
    """
    duplicate: duplicate_cls = duplicate_cls
    """
    duplicate command of graphics_objects.
    """
    child_object_type: graphics_objects_child = graphics_objects_child
    """
    child_object_type of graphics_objects.
    """
