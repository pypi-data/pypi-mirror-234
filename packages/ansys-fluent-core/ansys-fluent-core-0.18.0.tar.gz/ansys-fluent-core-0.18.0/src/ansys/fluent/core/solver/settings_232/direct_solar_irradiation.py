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
from .piecewise_linear import piecewise_linear as piecewise_linear_cls
from .polynomial import polynomial as polynomial_cls
from .user_defined_3 import user_defined as user_defined_cls
class direct_solar_irradiation(Group):
    """
    'direct_solar_irradiation' child.
    """

    fluent_name = "direct-solar-irradiation"

    child_names = \
        ['option', 'constant', 'piecewise_linear', 'polynomial',
         'user_defined']

    option: option_cls = option_cls
    """
    option child of direct_solar_irradiation.
    """
    constant: constant_cls = constant_cls
    """
    constant child of direct_solar_irradiation.
    """
    piecewise_linear: piecewise_linear_cls = piecewise_linear_cls
    """
    piecewise_linear child of direct_solar_irradiation.
    """
    polynomial: polynomial_cls = polynomial_cls
    """
    polynomial child of direct_solar_irradiation.
    """
    user_defined: user_defined_cls = user_defined_cls
    """
    user_defined child of direct_solar_irradiation.
    """
