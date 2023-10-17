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
from .network_child import network_child

class network(NamedObject[network_child], _NonCreatableNamedObjectMixin[network_child]):
    """
    'network' child.
    """

    fluent_name = "network"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list_cls = list_cls
    """
    list command of network.
    """
    list_properties: list_properties_cls = list_properties_cls
    """
    list_properties command of network.
    """
    duplicate: duplicate_cls = duplicate_cls
    """
    duplicate command of network.
    """
    child_object_type: network_child = network_child
    """
    child_object_type of network.
    """
