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
class heat_of_pyrolysis(Group):
    """
    'heat_of_pyrolysis' child.
    """

    fluent_name = "heat-of-pyrolysis"

    child_names = \
        ['option', 'constant', 'boussinesq', 'coefficients',
         'number_of_coefficients', 'piecewise_polynomial',
         'nasa_9_piecewise_polynomial', 'piecewise_linear', 'anisotropic',
         'orthotropic', 'var_class']

    option: option_cls = option_cls
    """
    option child of heat_of_pyrolysis.
    """
    constant: constant_cls = constant_cls
    """
    constant child of heat_of_pyrolysis.
    """
    boussinesq: boussinesq_cls = boussinesq_cls
    """
    boussinesq child of heat_of_pyrolysis.
    """
    coefficients: coefficients_cls = coefficients_cls
    """
    coefficients child of heat_of_pyrolysis.
    """
    number_of_coefficients: number_of_coefficients_cls = number_of_coefficients_cls
    """
    number_of_coefficients child of heat_of_pyrolysis.
    """
    piecewise_polynomial: piecewise_polynomial_cls = piecewise_polynomial_cls
    """
    piecewise_polynomial child of heat_of_pyrolysis.
    """
    nasa_9_piecewise_polynomial: nasa_9_piecewise_polynomial_cls = nasa_9_piecewise_polynomial_cls
    """
    nasa_9_piecewise_polynomial child of heat_of_pyrolysis.
    """
    piecewise_linear: piecewise_linear_cls = piecewise_linear_cls
    """
    piecewise_linear child of heat_of_pyrolysis.
    """
    anisotropic: anisotropic_cls = anisotropic_cls
    """
    anisotropic child of heat_of_pyrolysis.
    """
    orthotropic: orthotropic_cls = orthotropic_cls
    """
    orthotropic child of heat_of_pyrolysis.
    """
    var_class: var_class_cls = var_class_cls
    """
    var_class child of heat_of_pyrolysis.
    """
