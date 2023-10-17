#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .pressure_gradient_effects import pressure_gradient_effects as pressure_gradient_effects_cls
from .thermal_effects import thermal_effects as thermal_effects_cls
class enhanced_wall_treatment_options(Group):
    """
    'enhanced_wall_treatment_options' child.
    """

    fluent_name = "enhanced-wall-treatment-options"

    child_names = \
        ['pressure_gradient_effects', 'thermal_effects']

    pressure_gradient_effects: pressure_gradient_effects_cls = pressure_gradient_effects_cls
    """
    pressure_gradient_effects child of enhanced_wall_treatment_options.
    """
    thermal_effects: thermal_effects_cls = thermal_effects_cls
    """
    thermal_effects child of enhanced_wall_treatment_options.
    """
