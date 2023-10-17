#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .heat_of_surface_reactions import heat_of_surface_reactions as heat_of_surface_reactions_cls
from .mass_deposition_source import mass_deposition_source as mass_deposition_source_cls
from .reaction_diffusion_balance import reaction_diffusion_balance as reaction_diffusion_balance_cls
from .surface_reaction_aggresiveness_factor import surface_reaction_aggresiveness_factor as surface_reaction_aggresiveness_factor_cls
from .surface_reaction_rate_temperature_factor import surface_reaction_rate_temperature_factor as surface_reaction_rate_temperature_factor_cls
from .surface_reaction_solid_fraction import surface_reaction_solid_fraction as surface_reaction_solid_fraction_cls
class wall_surface_options(Group):
    """
    'wall_surface_options' child.
    """

    fluent_name = "wall-surface-options"

    child_names = \
        ['heat_of_surface_reactions', 'mass_deposition_source',
         'reaction_diffusion_balance',
         'surface_reaction_aggresiveness_factor',
         'surface_reaction_rate_temperature_factor',
         'surface_reaction_solid_fraction']

    heat_of_surface_reactions: heat_of_surface_reactions_cls = heat_of_surface_reactions_cls
    """
    heat_of_surface_reactions child of wall_surface_options.
    """
    mass_deposition_source: mass_deposition_source_cls = mass_deposition_source_cls
    """
    mass_deposition_source child of wall_surface_options.
    """
    reaction_diffusion_balance: reaction_diffusion_balance_cls = reaction_diffusion_balance_cls
    """
    reaction_diffusion_balance child of wall_surface_options.
    """
    surface_reaction_aggresiveness_factor: surface_reaction_aggresiveness_factor_cls = surface_reaction_aggresiveness_factor_cls
    """
    surface_reaction_aggresiveness_factor child of wall_surface_options.
    """
    surface_reaction_rate_temperature_factor: surface_reaction_rate_temperature_factor_cls = surface_reaction_rate_temperature_factor_cls
    """
    surface_reaction_rate_temperature_factor child of wall_surface_options.
    """
    surface_reaction_solid_fraction: surface_reaction_solid_fraction_cls = surface_reaction_solid_fraction_cls
    """
    surface_reaction_solid_fraction child of wall_surface_options.
    """
