#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .option_10 import option as option_cls
from .lewis_number import lewis_number as lewis_number_cls
from .value_1 import value as value_cls
from .species_diffusivity import species_diffusivity as species_diffusivity_cls
from .multicomponent import multicomponent as multicomponent_cls
from .user_defined_function import user_defined_function as user_defined_function_cls
class mass_diffusivity(Group):
    """
    'mass_diffusivity' child.
    """

    fluent_name = "mass-diffusivity"

    child_names = \
        ['option', 'lewis_number', 'value', 'species_diffusivity',
         'multicomponent', 'user_defined_function']

    option: option_cls = option_cls
    """
    option child of mass_diffusivity.
    """
    lewis_number: lewis_number_cls = lewis_number_cls
    """
    lewis_number child of mass_diffusivity.
    """
    value: value_cls = value_cls
    """
    value child of mass_diffusivity.
    """
    species_diffusivity: species_diffusivity_cls = species_diffusivity_cls
    """
    species_diffusivity child of mass_diffusivity.
    """
    multicomponent: multicomponent_cls = multicomponent_cls
    """
    multicomponent child of mass_diffusivity.
    """
    user_defined_function: user_defined_function_cls = user_defined_function_cls
    """
    user_defined_function child of mass_diffusivity.
    """
