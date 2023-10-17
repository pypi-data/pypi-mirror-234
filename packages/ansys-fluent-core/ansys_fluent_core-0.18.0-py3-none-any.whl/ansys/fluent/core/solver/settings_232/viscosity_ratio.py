#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .method_2 import method as method_cls
from .number_of_coeff import number_of_coeff as number_of_coeff_cls
from .function_of import function_of as function_of_cls
from .coefficients_1 import coefficients as coefficients_cls
from .value_1 import value as value_cls
from .piecewise_polynomial_1 import piecewise_polynomial as piecewise_polynomial_cls
from .piecewise_linear import piecewise_linear as piecewise_linear_cls
class viscosity_ratio(Group):
    """
    'viscosity_ratio' child.
    """

    fluent_name = "viscosity-ratio"

    child_names = \
        ['method', 'number_of_coeff', 'function_of', 'coefficients', 'value',
         'piecewise_polynomial', 'piecewise_linear']

    method: method_cls = method_cls
    """
    method child of viscosity_ratio.
    """
    number_of_coeff: number_of_coeff_cls = number_of_coeff_cls
    """
    number_of_coeff child of viscosity_ratio.
    """
    function_of: function_of_cls = function_of_cls
    """
    function_of child of viscosity_ratio.
    """
    coefficients: coefficients_cls = coefficients_cls
    """
    coefficients child of viscosity_ratio.
    """
    value: value_cls = value_cls
    """
    value child of viscosity_ratio.
    """
    piecewise_polynomial: piecewise_polynomial_cls = piecewise_polynomial_cls
    """
    piecewise_polynomial child of viscosity_ratio.
    """
    piecewise_linear: piecewise_linear_cls = piecewise_linear_cls
    """
    piecewise_linear child of viscosity_ratio.
    """
