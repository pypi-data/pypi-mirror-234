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
from .species_diffusivity_child import species_diffusivity_child

class multicomponent_child(NamedObject[species_diffusivity_child], _NonCreatableNamedObjectMixin[species_diffusivity_child]):
    """
    'child_object_type' of multicomponent.
    """

    fluent_name = "child-object-type"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list_cls = list_cls
    """
    list command of multicomponent_child.
    """
    list_properties: list_properties_cls = list_properties_cls
    """
    list_properties command of multicomponent_child.
    """
    duplicate: duplicate_cls = duplicate_cls
    """
    duplicate command of multicomponent_child.
    """
    child_object_type: species_diffusivity_child = species_diffusivity_child
    """
    child_object_type of multicomponent_child.
    """
