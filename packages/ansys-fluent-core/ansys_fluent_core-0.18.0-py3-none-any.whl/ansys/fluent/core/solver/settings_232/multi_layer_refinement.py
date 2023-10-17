#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .type import type as type_cls
from .layer_count import layer_count as layer_count_cls
from .boundary_list import boundary_list as boundary_list_cls
from .refine_mesh import refine_mesh as refine_mesh_cls
class multi_layer_refinement(Group):
    """
    Enter the multiple boundary layer refinement menu.
    """

    fluent_name = "multi-layer-refinement"

    child_names = \
        ['type', 'layer_count', 'boundary_list']

    type: type_cls = type_cls
    """
    type child of multi_layer_refinement.
    """
    layer_count: layer_count_cls = layer_count_cls
    """
    layer_count child of multi_layer_refinement.
    """
    boundary_list: boundary_list_cls = boundary_list_cls
    """
    boundary_list child of multi_layer_refinement.
    """
    command_names = \
        ['refine_mesh']

    refine_mesh: refine_mesh_cls = refine_mesh_cls
    """
    refine_mesh command of multi_layer_refinement.
    """
