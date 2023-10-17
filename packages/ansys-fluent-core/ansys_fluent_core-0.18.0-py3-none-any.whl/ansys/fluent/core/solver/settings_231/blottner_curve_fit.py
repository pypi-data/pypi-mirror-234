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
class blottner_curve_fit(Group):
    """
    'blottner_curve_fit' child.
    """

    fluent_name = "blottner-curve-fit"

    child_names = \
        ['a', 'b', 'c']

    a: a_cls = a_cls
    """
    a child of blottner_curve_fit.
    """
    b: b_cls = b_cls
    """
    b child of blottner_curve_fit.
    """
    c: c_cls = c_cls
    """
    c child of blottner_curve_fit.
    """
