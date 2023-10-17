#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .option_2 import option as option_cls
from .b import b as b_cls
from .reference_viscosity import reference_viscosity as reference_viscosity_cls
from .reference_temperature import reference_temperature as reference_temperature_cls
from .temperature_exponent import temperature_exponent as temperature_exponent_cls
class power_law(Group):
    """
    'power_law' child.
    """

    fluent_name = "power-law"

    child_names = \
        ['option', 'b', 'reference_viscosity', 'reference_temperature',
         'temperature_exponent']

    option: option_cls = option_cls
    """
    option child of power_law.
    """
    b: b_cls = b_cls
    """
    b child of power_law.
    """
    reference_viscosity: reference_viscosity_cls = reference_viscosity_cls
    """
    reference_viscosity child of power_law.
    """
    reference_temperature: reference_temperature_cls = reference_temperature_cls
    """
    reference_temperature child of power_law.
    """
    temperature_exponent: temperature_exponent_cls = temperature_exponent_cls
    """
    temperature_exponent child of power_law.
    """
