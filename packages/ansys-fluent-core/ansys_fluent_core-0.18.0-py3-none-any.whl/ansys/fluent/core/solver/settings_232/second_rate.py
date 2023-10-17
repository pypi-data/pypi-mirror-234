#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .pre_exponential_factor import pre_exponential_factor as pre_exponential_factor_cls
from .activation_energy import activation_energy as activation_energy_cls
from .weighting_factor import weighting_factor as weighting_factor_cls
class second_rate(Group):
    """
    'second_rate' child.
    """

    fluent_name = "second-rate"

    child_names = \
        ['pre_exponential_factor', 'activation_energy', 'weighting_factor']

    pre_exponential_factor: pre_exponential_factor_cls = pre_exponential_factor_cls
    """
    pre_exponential_factor child of second_rate.
    """
    activation_energy: activation_energy_cls = activation_energy_cls
    """
    activation_energy child of second_rate.
    """
    weighting_factor: weighting_factor_cls = weighting_factor_cls
    """
    weighting_factor child of second_rate.
    """
