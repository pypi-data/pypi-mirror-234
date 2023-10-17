#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .option import option as option_cls
from .constant import constant as constant_cls
from .coefficients import coefficients as coefficients_cls
from .number_of_coefficients import number_of_coefficients as number_of_coefficients_cls
from .piecewise_linear import piecewise_linear as piecewise_linear_cls
from .piecewise_polynomial import piecewise_polynomial as piecewise_polynomial_cls
class conductivity_2(Group):
    """
    'conductivity_2' child.
    """

    fluent_name = "conductivity-2"

    child_names = \
        ['option', 'constant', 'coefficients', 'number_of_coefficients',
         'piecewise_linear', 'piecewise_polynomial']

    option: option_cls = option_cls
    """
    option child of conductivity_2.
    """
    constant: constant_cls = constant_cls
    """
    constant child of conductivity_2.
    """
    coefficients: coefficients_cls = coefficients_cls
    """
    coefficients child of conductivity_2.
    """
    number_of_coefficients: number_of_coefficients_cls = number_of_coefficients_cls
    """
    number_of_coefficients child of conductivity_2.
    """
    piecewise_linear: piecewise_linear_cls = piecewise_linear_cls
    """
    piecewise_linear child of conductivity_2.
    """
    piecewise_polynomial: piecewise_polynomial_cls = piecewise_polynomial_cls
    """
    piecewise_polynomial child of conductivity_2.
    """
