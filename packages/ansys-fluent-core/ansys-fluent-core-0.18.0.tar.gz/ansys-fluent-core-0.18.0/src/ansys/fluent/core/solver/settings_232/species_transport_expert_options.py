#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .linearize_convection_source import linearize_convection_source as linearize_convection_source_cls
from .linearize_diffusion_source import linearize_diffusion_source as linearize_diffusion_source_cls
from .blending import blending as blending_cls
from .minimum_cell_quality_threshold import minimum_cell_quality_threshold as minimum_cell_quality_threshold_cls
class species_transport_expert_options(Group):
    """
    'species_transport_expert_options' child.
    """

    fluent_name = "species-transport-expert-options"

    child_names = \
        ['linearize_convection_source', 'linearize_diffusion_source',
         'blending', 'minimum_cell_quality_threshold']

    linearize_convection_source: linearize_convection_source_cls = linearize_convection_source_cls
    """
    linearize_convection_source child of species_transport_expert_options.
    """
    linearize_diffusion_source: linearize_diffusion_source_cls = linearize_diffusion_source_cls
    """
    linearize_diffusion_source child of species_transport_expert_options.
    """
    blending: blending_cls = blending_cls
    """
    blending child of species_transport_expert_options.
    """
    minimum_cell_quality_threshold: minimum_cell_quality_threshold_cls = minimum_cell_quality_threshold_cls
    """
    minimum_cell_quality_threshold child of species_transport_expert_options.
    """
