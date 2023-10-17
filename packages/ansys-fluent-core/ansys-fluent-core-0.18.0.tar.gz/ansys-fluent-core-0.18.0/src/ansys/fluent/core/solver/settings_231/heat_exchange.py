#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .computed_heat_rejection import computed_heat_rejection as computed_heat_rejection_cls
from .inlet_temperature import inlet_temperature as inlet_temperature_cls
from .outlet_temperature import outlet_temperature as outlet_temperature_cls
from .mass_flow_rate import mass_flow_rate as mass_flow_rate_cls
from .specific_heat_5 import specific_heat as specific_heat_cls
class heat_exchange(Group):
    """
    'heat_exchange' child.
    """

    fluent_name = "heat-exchange"

    command_names = \
        ['computed_heat_rejection', 'inlet_temperature', 'outlet_temperature',
         'mass_flow_rate', 'specific_heat']

    computed_heat_rejection: computed_heat_rejection_cls = computed_heat_rejection_cls
    """
    computed_heat_rejection command of heat_exchange.
    """
    inlet_temperature: inlet_temperature_cls = inlet_temperature_cls
    """
    inlet_temperature command of heat_exchange.
    """
    outlet_temperature: outlet_temperature_cls = outlet_temperature_cls
    """
    outlet_temperature command of heat_exchange.
    """
    mass_flow_rate: mass_flow_rate_cls = mass_flow_rate_cls
    """
    mass_flow_rate command of heat_exchange.
    """
    specific_heat: specific_heat_cls = specific_heat_cls
    """
    specific_heat command of heat_exchange.
    """
