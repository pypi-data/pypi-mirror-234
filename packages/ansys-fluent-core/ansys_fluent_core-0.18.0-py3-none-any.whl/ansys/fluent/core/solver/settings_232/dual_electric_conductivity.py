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
from .user_defined_function import user_defined_function as user_defined_function_cls
class dual_electric_conductivity(Group):
    """
    'dual_electric_conductivity' child.
    """

    fluent_name = "dual-electric-conductivity"

    child_names = \
        ['option', 'value', 'piecewise_linear', 'piecewise_polynomial',
         'polynomial', 'expression', 'user_defined_function']

    option: option_cls = option_cls
    """
    option child of dual_electric_conductivity.
    """
    value: value_cls = value_cls
    """
    value child of dual_electric_conductivity.
    """
    piecewise_linear: piecewise_linear_cls = piecewise_linear_cls
    """
    piecewise_linear child of dual_electric_conductivity.
    """
    piecewise_polynomial: piecewise_polynomial_cls = piecewise_polynomial_cls
    """
    piecewise_polynomial child of dual_electric_conductivity.
    """
    polynomial: polynomial_cls = polynomial_cls
    """
    polynomial child of dual_electric_conductivity.
    """
    expression: expression_cls = expression_cls
    """
    expression child of dual_electric_conductivity.
    """
    user_defined_function: user_defined_function_cls = user_defined_function_cls
    """
    user_defined_function child of dual_electric_conductivity.
    """
