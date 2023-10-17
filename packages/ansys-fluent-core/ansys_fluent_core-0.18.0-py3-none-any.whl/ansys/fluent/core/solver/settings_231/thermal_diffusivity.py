#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .option_9 import option as option_cls
from .species_diffusivity import species_diffusivity as species_diffusivity_cls
from .user_defined_function import user_defined_function as user_defined_function_cls
class thermal_diffusivity(Group):
    """
    'thermal_diffusivity' child.
    """

    fluent_name = "thermal-diffusivity"

    child_names = \
        ['option', 'species_diffusivity', 'user_defined_function']

    option: option_cls = option_cls
    """
    option child of thermal_diffusivity.
    """
    species_diffusivity: species_diffusivity_cls = species_diffusivity_cls
    """
    species_diffusivity child of thermal_diffusivity.
    """
    user_defined_function: user_defined_function_cls = user_defined_function_cls
    """
    user_defined_function child of thermal_diffusivity.
    """
