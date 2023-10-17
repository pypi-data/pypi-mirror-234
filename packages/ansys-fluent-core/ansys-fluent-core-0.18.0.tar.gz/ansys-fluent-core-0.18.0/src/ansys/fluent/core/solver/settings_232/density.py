#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .option_10 import option as option_cls
from .real_gas_nist import real_gas_nist as real_gas_nist_cls
from .value_1 import value as value_cls
from .compressible_liquid import compressible_liquid as compressible_liquid_cls
from .piecewise_linear import piecewise_linear as piecewise_linear_cls
from .piecewise_polynomial import piecewise_polynomial as piecewise_polynomial_cls
from .polynomial import polynomial as polynomial_cls
from .expression import expression as expression_cls
from .user_defined_function import user_defined_function as user_defined_function_cls
from .rgp_table import rgp_table as rgp_table_cls
class density(Group):
    """
    'density' child.
    """

    fluent_name = "density"

    child_names = \
        ['option', 'real_gas_nist', 'value', 'compressible_liquid',
         'piecewise_linear', 'piecewise_polynomial', 'polynomial',
         'expression', 'user_defined_function', 'rgp_table']

    option: option_cls = option_cls
    """
    option child of density.
    """
    real_gas_nist: real_gas_nist_cls = real_gas_nist_cls
    """
    real_gas_nist child of density.
    """
    value: value_cls = value_cls
    """
    value child of density.
    """
    compressible_liquid: compressible_liquid_cls = compressible_liquid_cls
    """
    compressible_liquid child of density.
    """
    piecewise_linear: piecewise_linear_cls = piecewise_linear_cls
    """
    piecewise_linear child of density.
    """
    piecewise_polynomial: piecewise_polynomial_cls = piecewise_polynomial_cls
    """
    piecewise_polynomial child of density.
    """
    polynomial: polynomial_cls = polynomial_cls
    """
    polynomial child of density.
    """
    expression: expression_cls = expression_cls
    """
    expression child of density.
    """
    user_defined_function: user_defined_function_cls = user_defined_function_cls
    """
    user_defined_function child of density.
    """
    rgp_table: rgp_table_cls = rgp_table_cls
    """
    rgp_table child of density.
    """
