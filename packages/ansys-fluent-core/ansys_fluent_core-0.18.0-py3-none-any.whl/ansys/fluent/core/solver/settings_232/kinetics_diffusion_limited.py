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
class kinetics_diffusion_limited(Group):
    """
    'kinetics_diffusion_limited' child.
    """

    fluent_name = "kinetics-diffusion-limited"

    child_names = \
        ['diffusion_rate_constant', 'pre_exponential_factor',
         'activation_energy']

    diffusion_rate_constant: diffusion_rate_constant_cls = diffusion_rate_constant_cls
    """
    diffusion_rate_constant child of kinetics_diffusion_limited.
    """
    pre_exponential_factor: pre_exponential_factor_cls = pre_exponential_factor_cls
    """
    pre_exponential_factor child of kinetics_diffusion_limited.
    """
    activation_energy: activation_energy_cls = activation_energy_cls
    """
    activation_energy child of kinetics_diffusion_limited.
    """
