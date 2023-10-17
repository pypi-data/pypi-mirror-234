#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .diffusion_rate_constant import diffusion_rate_constant as diffusion_rate_constant_cls
from .pre_exponential_factor import pre_exponential_factor as pre_exponential_factor_cls
from .activation_energy import activation_energy as activation_energy_cls
from .char_porosity import char_porosity as char_porosity_cls
from .mean_pore_radius import mean_pore_radius as mean_pore_radius_cls
from .specific_internal_surface_area import specific_internal_surface_area as specific_internal_surface_area_cls
from .tortuosity import tortuosity as tortuosity_cls
from .burning_mode import burning_mode as burning_mode_cls
class intrinsic_model(Group):
    """
    'intrinsic_model' child.
    """

    fluent_name = "intrinsic-model"

    child_names = \
        ['diffusion_rate_constant', 'pre_exponential_factor',
         'activation_energy', 'char_porosity', 'mean_pore_radius',
         'specific_internal_surface_area', 'tortuosity', 'burning_mode']

    diffusion_rate_constant: diffusion_rate_constant_cls = diffusion_rate_constant_cls
    """
    diffusion_rate_constant child of intrinsic_model.
    """
    pre_exponential_factor: pre_exponential_factor_cls = pre_exponential_factor_cls
    """
    pre_exponential_factor child of intrinsic_model.
    """
    activation_energy: activation_energy_cls = activation_energy_cls
    """
    activation_energy child of intrinsic_model.
    """
    char_porosity: char_porosity_cls = char_porosity_cls
    """
    char_porosity child of intrinsic_model.
    """
    mean_pore_radius: mean_pore_radius_cls = mean_pore_radius_cls
    """
    mean_pore_radius child of intrinsic_model.
    """
    specific_internal_surface_area: specific_internal_surface_area_cls = specific_internal_surface_area_cls
    """
    specific_internal_surface_area child of intrinsic_model.
    """
    tortuosity: tortuosity_cls = tortuosity_cls
    """
    tortuosity child of intrinsic_model.
    """
    burning_mode: burning_mode_cls = burning_mode_cls
    """
    burning_mode child of intrinsic_model.
    """
