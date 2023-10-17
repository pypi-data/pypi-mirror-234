#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .option_10 import option as option_cls
from .value_1 import value as value_cls
from .piecewise_linear import piecewise_linear as piecewise_linear_cls
from .piecewise_polynomial import piecewise_polynomial as piecewise_polynomial_cls
from .polynomial import polynomial as polynomial_cls
from .expression import expression as expression_cls
from .biaxial import biaxial as biaxial_cls
from .cyl_orthotropic_1 import cyl_orthotropic as cyl_orthotropic_cls
from .orthotropic_1 import orthotropic as orthotropic_cls
from .principal_axes_values import principal_axes_values as principal_axes_values_cls
from .anisotropic_1 import anisotropic as anisotropic_cls
from .user_defined_function import user_defined_function as user_defined_function_cls
class thermal_conductivity(Group):
    """
    'thermal_conductivity' child.
    """

    fluent_name = "thermal-conductivity"

    child_names = \
        ['option', 'value', 'piecewise_linear', 'piecewise_polynomial',
         'polynomial', 'expression', 'biaxial', 'cyl_orthotropic',
         'orthotropic', 'principal_axes_values', 'anisotropic',
         'user_defined_function']

    option: option_cls = option_cls
    """
    option child of thermal_conductivity.
    """
    value: value_cls = value_cls
    """
    value child of thermal_conductivity.
    """
    piecewise_linear: piecewise_linear_cls = piecewise_linear_cls
    """
    piecewise_linear child of thermal_conductivity.
    """
    piecewise_polynomial: piecewise_polynomial_cls = piecewise_polynomial_cls
    """
    piecewise_polynomial child of thermal_conductivity.
    """
    polynomial: polynomial_cls = polynomial_cls
    """
    polynomial child of thermal_conductivity.
    """
    expression: expression_cls = expression_cls
    """
    expression child of thermal_conductivity.
    """
    biaxial: biaxial_cls = biaxial_cls
    """
    biaxial child of thermal_conductivity.
    """
    cyl_orthotropic: cyl_orthotropic_cls = cyl_orthotropic_cls
    """
    cyl_orthotropic child of thermal_conductivity.
    """
    orthotropic: orthotropic_cls = orthotropic_cls
    """
    orthotropic child of thermal_conductivity.
    """
    principal_axes_values: principal_axes_values_cls = principal_axes_values_cls
    """
    principal_axes_values child of thermal_conductivity.
    """
    anisotropic: anisotropic_cls = anisotropic_cls
    """
    anisotropic child of thermal_conductivity.
    """
    user_defined_function: user_defined_function_cls = user_defined_function_cls
    """
    user_defined_function child of thermal_conductivity.
    """
