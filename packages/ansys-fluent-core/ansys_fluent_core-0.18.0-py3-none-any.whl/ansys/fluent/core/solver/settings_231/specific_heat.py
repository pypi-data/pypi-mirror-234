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
from .piecewise_linear import piecewise_linear as piecewise_linear_cls
from .piecewise_polynomial import piecewise_polynomial as piecewise_polynomial_cls
from .polynomial import polynomial as polynomial_cls
from .nasa_9_piecewise_polynomial import nasa_9_piecewise_polynomial as nasa_9_piecewise_polynomial_cls
from .user_defined_function import user_defined_function as user_defined_function_cls
from .rgp_table import rgp_table as rgp_table_cls
from .real_gas_nist import real_gas_nist as real_gas_nist_cls
class specific_heat(Group):
    """
    'specific_heat' child.
    """

    fluent_name = "specific-heat"

    child_names = \
        ['option', 'value', 'piecewise_linear', 'piecewise_polynomial',
         'polynomial', 'nasa_9_piecewise_polynomial', 'user_defined_function',
         'rgp_table', 'real_gas_nist']

    option: option_cls = option_cls
    """
    option child of specific_heat.
    """
    value: value_cls = value_cls
    """
    value child of specific_heat.
    """
    piecewise_linear: piecewise_linear_cls = piecewise_linear_cls
    """
    piecewise_linear child of specific_heat.
    """
    piecewise_polynomial: piecewise_polynomial_cls = piecewise_polynomial_cls
    """
    piecewise_polynomial child of specific_heat.
    """
    polynomial: polynomial_cls = polynomial_cls
    """
    polynomial child of specific_heat.
    """
    nasa_9_piecewise_polynomial: nasa_9_piecewise_polynomial_cls = nasa_9_piecewise_polynomial_cls
    """
    nasa_9_piecewise_polynomial child of specific_heat.
    """
    user_defined_function: user_defined_function_cls = user_defined_function_cls
    """
    user_defined_function child of specific_heat.
    """
    rgp_table: rgp_table_cls = rgp_table_cls
    """
    rgp_table child of specific_heat.
    """
    real_gas_nist: real_gas_nist_cls = real_gas_nist_cls
    """
    real_gas_nist child of specific_heat.
    """
