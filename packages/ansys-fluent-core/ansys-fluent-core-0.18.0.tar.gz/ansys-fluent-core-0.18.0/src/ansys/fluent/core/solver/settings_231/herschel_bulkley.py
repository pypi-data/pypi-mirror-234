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
from .yield_stress_threshold import yield_stress_threshold as yield_stress_threshold_cls
from .critical_shear_rate import critical_shear_rate as critical_shear_rate_cls
from .reference_temperature import reference_temperature as reference_temperature_cls
from .activation_energy import activation_energy as activation_energy_cls
class herschel_bulkley(Group):
    """
    'herschel_bulkley' child.
    """

    fluent_name = "herschel-bulkley"

    child_names = \
        ['option', 'consistency_index', 'power_law_index',
         'yield_stress_threshold', 'critical_shear_rate',
         'reference_temperature', 'activation_energy']

    option: option_cls = option_cls
    """
    option child of herschel_bulkley.
    """
    consistency_index: consistency_index_cls = consistency_index_cls
    """
    consistency_index child of herschel_bulkley.
    """
    power_law_index: power_law_index_cls = power_law_index_cls
    """
    power_law_index child of herschel_bulkley.
    """
    yield_stress_threshold: yield_stress_threshold_cls = yield_stress_threshold_cls
    """
    yield_stress_threshold child of herschel_bulkley.
    """
    critical_shear_rate: critical_shear_rate_cls = critical_shear_rate_cls
    """
    critical_shear_rate child of herschel_bulkley.
    """
    reference_temperature: reference_temperature_cls = reference_temperature_cls
    """
    reference_temperature child of herschel_bulkley.
    """
    activation_energy: activation_energy_cls = activation_energy_cls
    """
    activation_energy child of herschel_bulkley.
    """
