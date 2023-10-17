#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .variable_lewis_number import variable_lewis_number as variable_lewis_number_cls
from .use_vapor_species_heat_capacity import use_vapor_species_heat_capacity as use_vapor_species_heat_capacity_cls
class convection_diffusion_controlled(Group):
    """
    'convection_diffusion_controlled' child.
    """

    fluent_name = "convection-diffusion-controlled"

    child_names = \
        ['variable_lewis_number', 'use_vapor_species_heat_capacity']

    variable_lewis_number: variable_lewis_number_cls = variable_lewis_number_cls
    """
    variable_lewis_number child of convection_diffusion_controlled.
    """
    use_vapor_species_heat_capacity: use_vapor_species_heat_capacity_cls = use_vapor_species_heat_capacity_cls
    """
    use_vapor_species_heat_capacity child of convection_diffusion_controlled.
    """
