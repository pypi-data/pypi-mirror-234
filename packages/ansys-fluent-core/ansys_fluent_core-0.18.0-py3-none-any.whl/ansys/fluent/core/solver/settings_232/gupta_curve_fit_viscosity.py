#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .a import a as a_cls
from .b import b as b_cls
from .c import c as c_cls
class gupta_curve_fit_viscosity(Group):
    """
    'gupta_curve_fit_viscosity' child.
    """

    fluent_name = "gupta-curve-fit-viscosity"

    child_names = \
        ['a', 'b', 'c']

    a: a_cls = a_cls
    """
    a child of gupta_curve_fit_viscosity.
    """
    b: b_cls = b_cls
    """
    b child of gupta_curve_fit_viscosity.
    """
    c: c_cls = c_cls
    """
    c child of gupta_curve_fit_viscosity.
    """
