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
from .radiator_child import radiator_child

class radiator(NamedObject[radiator_child], _NonCreatableNamedObjectMixin[radiator_child]):
    """
    'radiator' child.
    """

    fluent_name = "radiator"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list_cls = list_cls
    """
    list command of radiator.
    """
    list_properties: list_properties_cls = list_properties_cls
    """
    list_properties command of radiator.
    """
    duplicate: duplicate_cls = duplicate_cls
    """
    duplicate command of radiator.
    """
    child_object_type: radiator_child = radiator_child
    """
    child_object_type of radiator.
    """
