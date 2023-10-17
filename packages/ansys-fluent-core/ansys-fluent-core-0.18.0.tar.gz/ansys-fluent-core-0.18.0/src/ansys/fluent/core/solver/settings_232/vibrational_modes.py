#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .vibrational_temperature_mode_1 import vibrational_temperature_mode_1 as vibrational_temperature_mode_1_cls
from .vibrational_degeneracy_mode_1 import vibrational_degeneracy_mode_1 as vibrational_degeneracy_mode_1_cls
from .vibrational_temperature_mode_2 import vibrational_temperature_mode_2 as vibrational_temperature_mode_2_cls
from .vibrational_degeneracy_mode_2 import vibrational_degeneracy_mode_2 as vibrational_degeneracy_mode_2_cls
from .vibrational_temperature_mode_3 import vibrational_temperature_mode_3 as vibrational_temperature_mode_3_cls
from .vibrational_degeneracy_mode_3 import vibrational_degeneracy_mode_3 as vibrational_degeneracy_mode_3_cls
class vibrational_modes(Group):
    """
    'vibrational_modes' child.
    """

    fluent_name = "vibrational-modes"

    child_names = \
        ['vibrational_temperature_mode_1', 'vibrational_degeneracy_mode_1',
         'vibrational_temperature_mode_2', 'vibrational_degeneracy_mode_2',
         'vibrational_temperature_mode_3', 'vibrational_degeneracy_mode_3']

    vibrational_temperature_mode_1: vibrational_temperature_mode_1_cls = vibrational_temperature_mode_1_cls
    """
    vibrational_temperature_mode_1 child of vibrational_modes.
    """
    vibrational_degeneracy_mode_1: vibrational_degeneracy_mode_1_cls = vibrational_degeneracy_mode_1_cls
    """
    vibrational_degeneracy_mode_1 child of vibrational_modes.
    """
    vibrational_temperature_mode_2: vibrational_temperature_mode_2_cls = vibrational_temperature_mode_2_cls
    """
    vibrational_temperature_mode_2 child of vibrational_modes.
    """
    vibrational_degeneracy_mode_2: vibrational_degeneracy_mode_2_cls = vibrational_degeneracy_mode_2_cls
    """
    vibrational_degeneracy_mode_2 child of vibrational_modes.
    """
    vibrational_temperature_mode_3: vibrational_temperature_mode_3_cls = vibrational_temperature_mode_3_cls
    """
    vibrational_temperature_mode_3 child of vibrational_modes.
    """
    vibrational_degeneracy_mode_3: vibrational_degeneracy_mode_3_cls = vibrational_degeneracy_mode_3_cls
    """
    vibrational_degeneracy_mode_3 child of vibrational_modes.
    """
