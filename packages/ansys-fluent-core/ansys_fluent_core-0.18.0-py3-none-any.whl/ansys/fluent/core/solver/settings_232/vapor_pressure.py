#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .option_10 import option as option_cls
from .piecewise_linear import piecewise_linear as piecewise_linear_cls
from .piecewise_polynomial import piecewise_polynomial as piecewise_polynomial_cls
from .polynomial import polynomial as polynomial_cls
from .value_1 import value as value_cls
from .rgp_table import rgp_table as rgp_table_cls
from .user_defined_function import user_defined_function as user_defined_function_cls
class vapor_pressure(Group):
    """
    'vapor_pressure' child.
    """

    fluent_name = "vapor-pressure"

    child_names = \
        ['option', 'piecewise_linear', 'piecewise_polynomial', 'polynomial',
         'value', 'rgp_table', 'user_defined_function']

    option: option_cls = option_cls
    """
    option child of vapor_pressure.
    """
    piecewise_linear: piecewise_linear_cls = piecewise_linear_cls
    """
    piecewise_linear child of vapor_pressure.
    """
    piecewise_polynomial: piecewise_polynomial_cls = piecewise_polynomial_cls
    """
    piecewise_polynomial child of vapor_pressure.
    """
    polynomial: polynomial_cls = polynomial_cls
    """
    polynomial child of vapor_pressure.
    """
    value: value_cls = value_cls
    """
    value child of vapor_pressure.
    """
    rgp_table: rgp_table_cls = rgp_table_cls
    """
    rgp_table child of vapor_pressure.
    """
    user_defined_function: user_defined_function_cls = user_defined_function_cls
    """
    user_defined_function child of vapor_pressure.
    """
