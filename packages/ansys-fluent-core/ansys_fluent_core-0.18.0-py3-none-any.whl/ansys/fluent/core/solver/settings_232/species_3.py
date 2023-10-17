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
from .species_child import species_child

class species(NamedObject[species_child], _NonCreatableNamedObjectMixin[species_child]):
    """
    'species' child.
    """

    fluent_name = "species"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list_cls = list_cls
    """
    list command of species.
    """
    list_properties: list_properties_cls = list_properties_cls
    """
    list_properties command of species.
    """
    duplicate: duplicate_cls = duplicate_cls
    """
    duplicate command of species.
    """
    child_object_type: species_child = species_child
    """
    child_object_type of species.
    """
