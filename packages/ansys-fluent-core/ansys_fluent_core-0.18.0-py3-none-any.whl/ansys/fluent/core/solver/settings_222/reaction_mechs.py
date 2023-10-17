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
class reaction_mechs(Group):
    """
    'reaction_mechs' child.
    """

    fluent_name = "reaction-mechs"

    child_names = \
        ['option', 'constant', 'boussinesq', 'coefficients',
         'number_of_coefficients', 'piecewise_polynomial',
         'nasa_9_piecewise_polynomial', 'piecewise_linear', 'anisotropic',
         'orthotropic', 'var_class']

    option: option_cls = option_cls
    """
    option child of reaction_mechs.
    """
    constant: constant_cls = constant_cls
    """
    constant child of reaction_mechs.
    """
    boussinesq: boussinesq_cls = boussinesq_cls
    """
    boussinesq child of reaction_mechs.
    """
    coefficients: coefficients_cls = coefficients_cls
    """
    coefficients child of reaction_mechs.
    """
    number_of_coefficients: number_of_coefficients_cls = number_of_coefficients_cls
    """
    number_of_coefficients child of reaction_mechs.
    """
    piecewise_polynomial: piecewise_polynomial_cls = piecewise_polynomial_cls
    """
    piecewise_polynomial child of reaction_mechs.
    """
    nasa_9_piecewise_polynomial: nasa_9_piecewise_polynomial_cls = nasa_9_piecewise_polynomial_cls
    """
    nasa_9_piecewise_polynomial child of reaction_mechs.
    """
    piecewise_linear: piecewise_linear_cls = piecewise_linear_cls
    """
    piecewise_linear child of reaction_mechs.
    """
    anisotropic: anisotropic_cls = anisotropic_cls
    """
    anisotropic child of reaction_mechs.
    """
    orthotropic: orthotropic_cls = orthotropic_cls
    """
    orthotropic child of reaction_mechs.
    """
    var_class: var_class_cls = var_class_cls
    """
    var_class child of reaction_mechs.
    """
