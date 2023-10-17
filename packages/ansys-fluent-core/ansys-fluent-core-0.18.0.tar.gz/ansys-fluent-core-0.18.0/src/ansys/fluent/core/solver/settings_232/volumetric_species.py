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
from .fluid_child import fluid_child

class volumetric_species(NamedObject[fluid_child], _CreatableNamedObjectMixin[fluid_child]):
    """
    'volumetric_species' child.
    """

    fluent_name = "volumetric-species"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list_cls = list_cls
    """
    list command of volumetric_species.
    """
    list_properties: list_properties_cls = list_properties_cls
    """
    list_properties command of volumetric_species.
    """
    duplicate: duplicate_cls = duplicate_cls
    """
    duplicate command of volumetric_species.
    """
    child_object_type: fluid_child = fluid_child
    """
    child_object_type of volumetric_species.
    """
