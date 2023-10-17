#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .option_2 import option as option_cls
from .consistency_index import consistency_index as consistency_index_cls
from .power_law_index import power_law_index as power_law_index_cls
from .minimum_viscosity import minimum_viscosity as minimum_viscosity_cls
from .maximum_viscosity import maximum_viscosity as maximum_viscosity_cls
from .reference_temperature import reference_temperature as reference_temperature_cls
from .activation_energy import activation_energy as activation_energy_cls
class non_newtonian_power_law(Group):
    """
    'non_newtonian_power_law' child.
    """

    fluent_name = "non-newtonian-power-law"

    child_names = \
        ['option', 'consistency_index', 'power_law_index',
         'minimum_viscosity', 'maximum_viscosity', 'reference_temperature',
         'activation_energy']

    option: option_cls = option_cls
    """
    option child of non_newtonian_power_law.
    """
    consistency_index: consistency_index_cls = consistency_index_cls
    """
    consistency_index child of non_newtonian_power_law.
    """
    power_law_index: power_law_index_cls = power_law_index_cls
    """
    power_law_index child of non_newtonian_power_law.
    """
    minimum_viscosity: minimum_viscosity_cls = minimum_viscosity_cls
    """
    minimum_viscosity child of non_newtonian_power_law.
    """
    maximum_viscosity: maximum_viscosity_cls = maximum_viscosity_cls
    """
    maximum_viscosity child of non_newtonian_power_law.
    """
    reference_temperature: reference_temperature_cls = reference_temperature_cls
    """
    reference_temperature child of non_newtonian_power_law.
    """
    activation_energy: activation_energy_cls = activation_energy_cls
    """
    activation_energy child of non_newtonian_power_law.
    """
