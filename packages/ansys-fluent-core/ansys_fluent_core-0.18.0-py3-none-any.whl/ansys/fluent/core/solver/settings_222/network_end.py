#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .change_type import change_type as change_type_cls
from .network_end_child import network_end_child

class network_end(NamedObject[network_end_child], _CreatableNamedObjectMixin[network_end_child]):
    """
    'network_end' child.
    """

    fluent_name = "network-end"

    command_names = \
        ['change_type']

    change_type: change_type_cls = change_type_cls
    """
    change_type command of network_end.
    """
    child_object_type: network_end_child = network_end_child
    """
    child_object_type of network_end.
    """
