#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .parts import parts as parts_cls
from .list_topology import list_topology as list_topology_cls
class geometry(Group):
    """
    'geometry' child.
    """

    fluent_name = "geometry"

    child_names = \
        ['parts']

    parts: parts_cls = parts_cls
    """
    parts child of geometry.
    """
    command_names = \
        ['list_topology']

    list_topology: list_topology_cls = list_topology_cls
    """
    list_topology command of geometry.
    """
