#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .type_5 import type as type_cls
from .boundary_1 import boundary_1 as boundary_1_cls
from .boundary_2 import boundary_2 as boundary_2_cls
from .periodicity import periodicity as periodicity_cls
from .mesh_connectivity import mesh_connectivity as mesh_connectivity_cls
class interfaces_child(Group):
    """
    'child_object_type' of interfaces.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['type', 'boundary_1', 'boundary_2', 'periodicity',
         'mesh_connectivity']

    type: type_cls = type_cls
    """
    type child of interfaces_child.
    """
    boundary_1: boundary_1_cls = boundary_1_cls
    """
    boundary_1 child of interfaces_child.
    """
    boundary_2: boundary_2_cls = boundary_2_cls
    """
    boundary_2 child of interfaces_child.
    """
    periodicity: periodicity_cls = periodicity_cls
    """
    periodicity child of interfaces_child.
    """
    mesh_connectivity: mesh_connectivity_cls = mesh_connectivity_cls
    """
    mesh_connectivity child of interfaces_child.
    """
