#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .use_vapor_species_heat_capacity import use_vapor_species_heat_capacity as use_vapor_species_heat_capacity_cls
class diffusion_controlled(Group):
    """
    'diffusion_controlled' child.
    """

    fluent_name = "diffusion-controlled"

    child_names = \
        ['use_vapor_species_heat_capacity']

    use_vapor_species_heat_capacity: use_vapor_species_heat_capacity_cls = use_vapor_species_heat_capacity_cls
    """
    use_vapor_species_heat_capacity child of diffusion_controlled.
    """
