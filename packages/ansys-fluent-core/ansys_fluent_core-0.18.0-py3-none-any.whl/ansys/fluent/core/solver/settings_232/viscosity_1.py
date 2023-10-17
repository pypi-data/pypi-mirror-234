#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .option_10 import option as option_cls
from .value_1 import value as value_cls
from .piecewise_linear import piecewise_linear as piecewise_linear_cls
from .piecewise_polynomial import piecewise_polynomial as piecewise_polynomial_cls
from .polynomial import polynomial as polynomial_cls
from .expression import expression as expression_cls
from .power_law import power_law as power_law_cls
from .sutherland import sutherland as sutherland_cls
from .user_defined_function import user_defined_function as user_defined_function_cls
from .real_gas_nist_mixture import real_gas_nist_mixture as real_gas_nist_mixture_cls
class viscosity(Group):
    """
    'viscosity' child.
    """

    fluent_name = "viscosity"

    child_names = \
        ['option', 'value', 'piecewise_linear', 'piecewise_polynomial',
         'polynomial', 'expression', 'power_law', 'sutherland',
         'user_defined_function', 'real_gas_nist_mixture']

    option: option_cls = option_cls
    """
    option child of viscosity.
    """
    value: value_cls = value_cls
    """
    value child of viscosity.
    """
    piecewise_linear: piecewise_linear_cls = piecewise_linear_cls
    """
    piecewise_linear child of viscosity.
    """
    piecewise_polynomial: piecewise_polynomial_cls = piecewise_polynomial_cls
    """
    piecewise_polynomial child of viscosity.
    """
    polynomial: polynomial_cls = polynomial_cls
    """
    polynomial child of viscosity.
    """
    expression: expression_cls = expression_cls
    """
    expression child of viscosity.
    """
    power_law: power_law_cls = power_law_cls
    """
    power_law child of viscosity.
    """
    sutherland: sutherland_cls = sutherland_cls
    """
    sutherland child of viscosity.
    """
    user_defined_function: user_defined_function_cls = user_defined_function_cls
    """
    user_defined_function child of viscosity.
    """
    real_gas_nist_mixture: real_gas_nist_mixture_cls = real_gas_nist_mixture_cls
    """
    real_gas_nist_mixture child of viscosity.
    """
