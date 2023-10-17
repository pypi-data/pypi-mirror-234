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
from .iso_surface_child import iso_surface_child

class iso_surface(NamedObject[iso_surface_child], _CreatableNamedObjectMixin[iso_surface_child]):
    """
    'iso_surface' child.
    """

    fluent_name = "iso-surface"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list_cls = list_cls
    """
    list command of iso_surface.
    """
    list_properties: list_properties_cls = list_properties_cls
    """
    list_properties command of iso_surface.
    """
    duplicate: duplicate_cls = duplicate_cls
    """
    duplicate command of iso_surface.
    """
    child_object_type: iso_surface_child = iso_surface_child
    """
    child_object_type of iso_surface.
    """
