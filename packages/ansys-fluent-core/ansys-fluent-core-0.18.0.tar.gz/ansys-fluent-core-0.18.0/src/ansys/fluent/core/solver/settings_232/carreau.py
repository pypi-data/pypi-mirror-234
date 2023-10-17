#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .option import option as option_cls
from .time_constant import time_constant as time_constant_cls
from .power_law_index import power_law_index as power_law_index_cls
from .zero_shear_viscosity import zero_shear_viscosity as zero_shear_viscosity_cls
from .infinite_shear_viscosity import infinite_shear_viscosity as infinite_shear_viscosity_cls
from .reference_temperature import reference_temperature as reference_temperature_cls
from .activation_energy import activation_energy as activation_energy_cls
class carreau(Group):
    """
    'carreau' child.
    """

    fluent_name = "carreau"

    child_names = \
        ['option', 'time_constant', 'power_law_index', 'zero_shear_viscosity',
         'infinite_shear_viscosity', 'reference_temperature',
         'activation_energy']

    option: option_cls = option_cls
    """
    option child of carreau.
    """
    time_constant: time_constant_cls = time_constant_cls
    """
    time_constant child of carreau.
    """
    power_law_index: power_law_index_cls = power_law_index_cls
    """
    power_law_index child of carreau.
    """
    zero_shear_viscosity: zero_shear_viscosity_cls = zero_shear_viscosity_cls
    """
    zero_shear_viscosity child of carreau.
    """
    infinite_shear_viscosity: infinite_shear_viscosity_cls = infinite_shear_viscosity_cls
    """
    infinite_shear_viscosity child of carreau.
    """
    reference_temperature: reference_temperature_cls = reference_temperature_cls
    """
    reference_temperature child of carreau.
    """
    activation_energy: activation_energy_cls = activation_energy_cls
    """
    activation_energy child of carreau.
    """
