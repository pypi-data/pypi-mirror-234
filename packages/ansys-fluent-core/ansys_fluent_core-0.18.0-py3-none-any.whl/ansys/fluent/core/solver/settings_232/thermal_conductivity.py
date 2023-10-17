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
from .gupta_curve_fit_conductivity import gupta_curve_fit_conductivity as gupta_curve_fit_conductivity_cls
from .expression import expression as expression_cls
from .user_defined_function import user_defined_function as user_defined_function_cls
from .rgp_table import rgp_table as rgp_table_cls
from .real_gas_nist import real_gas_nist as real_gas_nist_cls
class thermal_conductivity(Group):
    """
    'thermal_conductivity' child.
    """

    fluent_name = "thermal-conductivity"

    child_names = \
        ['option', 'value', 'piecewise_linear', 'piecewise_polynomial',
         'polynomial', 'gupta_curve_fit_conductivity', 'expression',
         'user_defined_function', 'rgp_table', 'real_gas_nist']

    option: option_cls = option_cls
    """
    option child of thermal_conductivity.
    """
    value: value_cls = value_cls
    """
    value child of thermal_conductivity.
    """
    piecewise_linear: piecewise_linear_cls = piecewise_linear_cls
    """
    piecewise_linear child of thermal_conductivity.
    """
    piecewise_polynomial: piecewise_polynomial_cls = piecewise_polynomial_cls
    """
    piecewise_polynomial child of thermal_conductivity.
    """
    polynomial: polynomial_cls = polynomial_cls
    """
    polynomial child of thermal_conductivity.
    """
    gupta_curve_fit_conductivity: gupta_curve_fit_conductivity_cls = gupta_curve_fit_conductivity_cls
    """
    gupta_curve_fit_conductivity child of thermal_conductivity.
    """
    expression: expression_cls = expression_cls
    """
    expression child of thermal_conductivity.
    """
    user_defined_function: user_defined_function_cls = user_defined_function_cls
    """
    user_defined_function child of thermal_conductivity.
    """
    rgp_table: rgp_table_cls = rgp_table_cls
    """
    rgp_table child of thermal_conductivity.
    """
    real_gas_nist: real_gas_nist_cls = real_gas_nist_cls
    """
    real_gas_nist child of thermal_conductivity.
    """
