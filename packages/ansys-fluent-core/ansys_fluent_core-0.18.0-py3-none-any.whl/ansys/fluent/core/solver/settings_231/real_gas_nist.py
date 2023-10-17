#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .nist_fluid import nist_fluid as nist_fluid_cls
from .lookup_table import lookup_table as lookup_table_cls
from .pressure_points import pressure_points as pressure_points_cls
from .pressure_minimum import pressure_minimum as pressure_minimum_cls
from .pressure_maximum import pressure_maximum as pressure_maximum_cls
from .temperature_points import temperature_points as temperature_points_cls
from .temperature_minimum import temperature_minimum as temperature_minimum_cls
from .temperature_maximum import temperature_maximum as temperature_maximum_cls
from .saturation_points import saturation_points as saturation_points_cls
class real_gas_nist(Group):
    """
    'real_gas_nist' child.
    """

    fluent_name = "real-gas-nist"

    child_names = \
        ['nist_fluid', 'lookup_table', 'pressure_points', 'pressure_minimum',
         'pressure_maximum', 'temperature_points', 'temperature_minimum',
         'temperature_maximum', 'saturation_points']

    nist_fluid: nist_fluid_cls = nist_fluid_cls
    """
    nist_fluid child of real_gas_nist.
    """
    lookup_table: lookup_table_cls = lookup_table_cls
    """
    lookup_table child of real_gas_nist.
    """
    pressure_points: pressure_points_cls = pressure_points_cls
    """
    pressure_points child of real_gas_nist.
    """
    pressure_minimum: pressure_minimum_cls = pressure_minimum_cls
    """
    pressure_minimum child of real_gas_nist.
    """
    pressure_maximum: pressure_maximum_cls = pressure_maximum_cls
    """
    pressure_maximum child of real_gas_nist.
    """
    temperature_points: temperature_points_cls = temperature_points_cls
    """
    temperature_points child of real_gas_nist.
    """
    temperature_minimum: temperature_minimum_cls = temperature_minimum_cls
    """
    temperature_minimum child of real_gas_nist.
    """
    temperature_maximum: temperature_maximum_cls = temperature_maximum_cls
    """
    temperature_maximum child of real_gas_nist.
    """
    saturation_points: saturation_points_cls = saturation_points_cls
    """
    saturation_points child of real_gas_nist.
    """
