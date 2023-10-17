#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .option_9 import option as option_cls
from .value import value as value_cls
from .user_defined_function import user_defined_function as user_defined_function_cls
from .combustion_mixture import combustion_mixture as combustion_mixture_cls
class premix_laminar_speed(Group):
    """
    'premix_laminar_speed' child.
    """

    fluent_name = "premix-laminar-speed"

    child_names = \
        ['option', 'value', 'user_defined_function', 'combustion_mixture']

    option: option_cls = option_cls
    """
    option child of premix_laminar_speed.
    """
    value: value_cls = value_cls
    """
    value child of premix_laminar_speed.
    """
    user_defined_function: user_defined_function_cls = user_defined_function_cls
    """
    user_defined_function child of premix_laminar_speed.
    """
    combustion_mixture: combustion_mixture_cls = combustion_mixture_cls
    """
    combustion_mixture child of premix_laminar_speed.
    """
