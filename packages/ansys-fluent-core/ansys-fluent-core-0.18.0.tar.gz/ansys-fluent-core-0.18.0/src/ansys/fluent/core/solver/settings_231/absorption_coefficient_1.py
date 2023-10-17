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
from .expression import expression as expression_cls
from .path_length import path_length as path_length_cls
from .gray_band_coefficients import gray_band_coefficients as gray_band_coefficients_cls
from .user_defined_function import user_defined_function as user_defined_function_cls
class absorption_coefficient(Group):
    """
    'absorption_coefficient' child.
    """

    fluent_name = "absorption-coefficient"

    child_names = \
        ['option', 'value', 'piecewise_linear', 'piecewise_polynomial',
         'polynomial', 'expression', 'path_length', 'gray_band_coefficients',
         'user_defined_function']

    option: option_cls = option_cls
    """
    option child of absorption_coefficient.
    """
    value: value_cls = value_cls
    """
    value child of absorption_coefficient.
    """
    piecewise_linear: piecewise_linear_cls = piecewise_linear_cls
    """
    piecewise_linear child of absorption_coefficient.
    """
    piecewise_polynomial: piecewise_polynomial_cls = piecewise_polynomial_cls
    """
    piecewise_polynomial child of absorption_coefficient.
    """
    polynomial: polynomial_cls = polynomial_cls
    """
    polynomial child of absorption_coefficient.
    """
    expression: expression_cls = expression_cls
    """
    expression child of absorption_coefficient.
    """
    path_length: path_length_cls = path_length_cls
    """
    path_length child of absorption_coefficient.
    """
    gray_band_coefficients: gray_band_coefficients_cls = gray_band_coefficients_cls
    """
    gray_band_coefficients child of absorption_coefficient.
    """
    user_defined_function: user_defined_function_cls = user_defined_function_cls
    """
    user_defined_function child of absorption_coefficient.
    """
