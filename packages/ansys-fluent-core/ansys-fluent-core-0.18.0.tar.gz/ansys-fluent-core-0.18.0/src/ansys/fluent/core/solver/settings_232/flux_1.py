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
from .flux_child import flux_child

class flux(NamedObject[flux_child], _CreatableNamedObjectMixin[flux_child]):
    """
    'flux' child.
    """

    fluent_name = "flux"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list_cls = list_cls
    """
    list command of flux.
    """
    list_properties: list_properties_cls = list_properties_cls
    """
    list_properties command of flux.
    """
    duplicate: duplicate_cls = duplicate_cls
    """
    duplicate command of flux.
    """
    child_object_type: flux_child = flux_child
    """
    child_object_type of flux.
    """
