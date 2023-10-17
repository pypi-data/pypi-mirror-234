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
from .delta_eddington import delta_eddington as delta_eddington_cls
from .user_defined_function import user_defined_function as user_defined_function_cls
class scattering_phase_function(Group):
    """
    'scattering_phase_function' child.
    """

    fluent_name = "scattering-phase-function"

    child_names = \
        ['option', 'value', 'delta_eddington', 'user_defined_function']

    option: option_cls = option_cls
    """
    option child of scattering_phase_function.
    """
    value: value_cls = value_cls
    """
    value child of scattering_phase_function.
    """
    delta_eddington: delta_eddington_cls = delta_eddington_cls
    """
    delta_eddington child of scattering_phase_function.
    """
    user_defined_function: user_defined_function_cls = user_defined_function_cls
    """
    user_defined_function child of scattering_phase_function.
    """
