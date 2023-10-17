#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .refine_mesh import refine_mesh as refine_mesh_cls
from .boundary_zones import boundary_zones as boundary_zones_cls
from .layer_count import layer_count as layer_count_cls
from .parameters import parameters as parameters_cls
class multi_layer_refinement(Group):
    """
    Enter the multiple boundary layer refinement menu.
    """

    fluent_name = "multi-layer-refinement"

    command_names = \
        ['refine_mesh', 'boundary_zones', 'layer_count', 'parameters']

    refine_mesh: refine_mesh_cls = refine_mesh_cls
    """
    refine_mesh command of multi_layer_refinement.
    """
    boundary_zones: boundary_zones_cls = boundary_zones_cls
    """
    boundary_zones command of multi_layer_refinement.
    """
    layer_count: layer_count_cls = layer_count_cls
    """
    layer_count command of multi_layer_refinement.
    """
    parameters: parameters_cls = parameters_cls
    """
    parameters command of multi_layer_refinement.
    """
