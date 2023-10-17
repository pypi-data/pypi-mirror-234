#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .viscous_terms import viscous_terms as viscous_terms_cls
from .species_reactions import species_reactions as species_reactions_cls
from .set_turbulent_viscosity_ratio import set_turbulent_viscosity_ratio as set_turbulent_viscosity_ratio_cls
from .reset_to_defaults import reset_to_defaults as reset_to_defaults_cls
class fmg_options(Group):
    """
    Enter the full-multigrid option menu.
    """

    fluent_name = "fmg-options"

    child_names = \
        ['viscous_terms', 'species_reactions',
         'set_turbulent_viscosity_ratio', 'reset_to_defaults']

    viscous_terms: viscous_terms_cls = viscous_terms_cls
    """
    viscous_terms child of fmg_options.
    """
    species_reactions: species_reactions_cls = species_reactions_cls
    """
    species_reactions child of fmg_options.
    """
    set_turbulent_viscosity_ratio: set_turbulent_viscosity_ratio_cls = set_turbulent_viscosity_ratio_cls
    """
    set_turbulent_viscosity_ratio child of fmg_options.
    """
    reset_to_defaults: reset_to_defaults_cls = reset_to_defaults_cls
    """
    reset_to_defaults child of fmg_options.
    """
