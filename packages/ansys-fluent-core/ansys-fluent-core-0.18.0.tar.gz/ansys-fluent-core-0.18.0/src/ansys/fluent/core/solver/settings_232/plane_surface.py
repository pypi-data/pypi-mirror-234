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
from .plane_surface_child import plane_surface_child

class plane_surface(NamedObject[plane_surface_child], _CreatableNamedObjectMixin[plane_surface_child]):
    """
    'plane_surface' child.
    """

    fluent_name = "plane-surface"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list_cls = list_cls
    """
    list command of plane_surface.
    """
    list_properties: list_properties_cls = list_properties_cls
    """
    list_properties command of plane_surface.
    """
    duplicate: duplicate_cls = duplicate_cls
    """
    duplicate command of plane_surface.
    """
    child_object_type: plane_surface_child = plane_surface_child
    """
    child_object_type of plane_surface.
    """
