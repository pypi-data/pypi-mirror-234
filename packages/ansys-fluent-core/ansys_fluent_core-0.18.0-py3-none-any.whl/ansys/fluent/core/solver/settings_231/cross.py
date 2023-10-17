#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .option_2 import option as option_cls
from .zero_shear_viscosity import zero_shear_viscosity as zero_shear_viscosity_cls
from .power_law_index import power_law_index as power_law_index_cls
from .time_constant import time_constant as time_constant_cls
from .reference_temperature import reference_temperature as reference_temperature_cls
from .activation_energy import activation_energy as activation_energy_cls
class cross(Group):
    """
    'cross' child.
    """

    fluent_name = "cross"

    child_names = \
        ['option', 'zero_shear_viscosity', 'power_law_index', 'time_constant',
         'reference_temperature', 'activation_energy']

    option: option_cls = option_cls
    """
    option child of cross.
    """
    zero_shear_viscosity: zero_shear_viscosity_cls = zero_shear_viscosity_cls
    """
    zero_shear_viscosity child of cross.
    """
    power_law_index: power_law_index_cls = power_law_index_cls
    """
    power_law_index child of cross.
    """
    time_constant: time_constant_cls = time_constant_cls
    """
    time_constant child of cross.
    """
    reference_temperature: reference_temperature_cls = reference_temperature_cls
    """
    reference_temperature child of cross.
    """
    activation_energy: activation_energy_cls = activation_energy_cls
    """
    activation_energy child of cross.
    """
