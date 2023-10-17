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
from .rake_surface_child import rake_surface_child

class rake_surface(NamedObject[rake_surface_child], _CreatableNamedObjectMixin[rake_surface_child]):
    """
    'rake_surface' child.
    """

    fluent_name = "rake-surface"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list_cls = list_cls
    """
    list command of rake_surface.
    """
    list_properties: list_properties_cls = list_properties_cls
    """
    list_properties command of rake_surface.
    """
    duplicate: duplicate_cls = duplicate_cls
    """
    duplicate command of rake_surface.
    """
    child_object_type: rake_surface_child = rake_surface_child
    """
    child_object_type of rake_surface.
    """
