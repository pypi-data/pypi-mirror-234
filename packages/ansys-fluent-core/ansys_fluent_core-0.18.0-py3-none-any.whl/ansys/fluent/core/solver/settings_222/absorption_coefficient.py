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
from .boussinesq import boussinesq as boussinesq_cls
from .coefficients import coefficients as coefficients_cls
from .number_of_coefficients import number_of_coefficients as number_of_coefficients_cls
from .piecewise_polynomial import piecewise_polynomial as piecewise_polynomial_cls
from .nasa_9_piecewise_polynomial import nasa_9_piecewise_polynomial as nasa_9_piecewise_polynomial_cls
from .piecewise_linear import piecewise_linear as piecewise_linear_cls
from .anisotropic import anisotropic as anisotropic_cls
from .orthotropic import orthotropic as orthotropic_cls
from .var_class import var_class as var_class_cls
class absorption_coefficient(Group):
    """
    'absorption_coefficient' child.
    """

    fluent_name = "absorption-coefficient"

    child_names = \
        ['option', 'constant', 'boussinesq', 'coefficients',
         'number_of_coefficients', 'piecewise_polynomial',
         'nasa_9_piecewise_polynomial', 'piecewise_linear', 'anisotropic',
         'orthotropic', 'var_class']

    option: option_cls = option_cls
    """
    option child of absorption_coefficient.
    """
    constant: constant_cls = constant_cls
    """
    constant child of absorption_coefficient.
    """
    boussinesq: boussinesq_cls = boussinesq_cls
    """
    boussinesq child of absorption_coefficient.
    """
    coefficients: coefficients_cls = coefficients_cls
    """
    coefficients child of absorption_coefficient.
    """
    number_of_coefficients: number_of_coefficients_cls = number_of_coefficients_cls
    """
    number_of_coefficients child of absorption_coefficient.
    """
    piecewise_polynomial: piecewise_polynomial_cls = piecewise_polynomial_cls
    """
    piecewise_polynomial child of absorption_coefficient.
    """
    nasa_9_piecewise_polynomial: nasa_9_piecewise_polynomial_cls = nasa_9_piecewise_polynomial_cls
    """
    nasa_9_piecewise_polynomial child of absorption_coefficient.
    """
    piecewise_linear: piecewise_linear_cls = piecewise_linear_cls
    """
    piecewise_linear child of absorption_coefficient.
    """
    anisotropic: anisotropic_cls = anisotropic_cls
    """
    anisotropic child of absorption_coefficient.
    """
    orthotropic: orthotropic_cls = orthotropic_cls
    """
    orthotropic child of absorption_coefficient.
    """
    var_class: var_class_cls = var_class_cls
    """
    var_class child of absorption_coefficient.
    """
