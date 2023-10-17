#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .minimum_1 import minimum as minimum_cls
from .maximum_1 import maximum as maximum_cls
from .number_of_coeff import number_of_coeff as number_of_coeff_cls
from .coefficients_1 import coefficients as coefficients_cls
class piecewise_polynomial_child(Group):
    """
    'child_object_type' of piecewise_polynomial.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['minimum', 'maximum', 'number_of_coeff', 'coefficients']

    minimum: minimum_cls = minimum_cls
    """
    minimum child of piecewise_polynomial_child.
    """
    maximum: maximum_cls = maximum_cls
    """
    maximum child of piecewise_polynomial_child.
    """
    number_of_coeff: number_of_coeff_cls = number_of_coeff_cls
    """
    number_of_coeff child of piecewise_polynomial_child.
    """
    coefficients: coefficients_cls = coefficients_cls
    """
    coefficients child of piecewise_polynomial_child.
    """
