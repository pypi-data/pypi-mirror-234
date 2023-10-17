#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .option_9 import option as option_cls
from .vibrational_modes import vibrational_modes as vibrational_modes_cls
from .value import value as value_cls
class characteristic_vibrational_temperature(Group):
    """
    'characteristic_vibrational_temperature' child.
    """

    fluent_name = "characteristic-vibrational-temperature"

    child_names = \
        ['option', 'vibrational_modes', 'value']

    option: option_cls = option_cls
    """
    option child of characteristic_vibrational_temperature.
    """
    vibrational_modes: vibrational_modes_cls = vibrational_modes_cls
    """
    vibrational_modes child of characteristic_vibrational_temperature.
    """
    value: value_cls = value_cls
    """
    value child of characteristic_vibrational_temperature.
    """
