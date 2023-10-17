#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .method import method as method_cls
from .number_of_coeff import number_of_coeff as number_of_coeff_cls
from .function_of import function_of as function_of_cls
from .coefficients import coefficients as coefficients_cls
from .constant import constant as constant_cls
from .piecewise_polynomial import piecewise_polynomial as piecewise_polynomial_cls
from .piecewise_linear import piecewise_linear as piecewise_linear_cls
class b(Group):
    """
    'b' child.
    """

    fluent_name = "b"

    child_names = \
        ['method', 'number_of_coeff', 'function_of', 'coefficients',
         'constant', 'piecewise_polynomial', 'piecewise_linear']

    method: method_cls = method_cls
    """
    method child of b.
    """
    number_of_coeff: number_of_coeff_cls = number_of_coeff_cls
    """
    number_of_coeff child of b.
    """
    function_of: function_of_cls = function_of_cls
    """
    function_of child of b.
    """
    coefficients: coefficients_cls = coefficients_cls
    """
    coefficients child of b.
    """
    constant: constant_cls = constant_cls
    """
    constant child of b.
    """
    piecewise_polynomial: piecewise_polynomial_cls = piecewise_polynomial_cls
    """
    piecewise_polynomial child of b.
    """
    piecewise_linear: piecewise_linear_cls = piecewise_linear_cls
    """
    piecewise_linear child of b.
    """
