#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .option_9 import option as option_cls
from .real_gas_nist_mixture import real_gas_nist_mixture as real_gas_nist_mixture_cls
from .user_defined_function import user_defined_function as user_defined_function_cls
class density(Group):
    """
    'density' child.
    """

    fluent_name = "density"

    child_names = \
        ['option', 'real_gas_nist_mixture', 'user_defined_function']

    option: option_cls = option_cls
    """
    option child of density.
    """
    real_gas_nist_mixture: real_gas_nist_mixture_cls = real_gas_nist_mixture_cls
    """
    real_gas_nist_mixture child of density.
    """
    user_defined_function: user_defined_function_cls = user_defined_function_cls
    """
    user_defined_function child of density.
    """
