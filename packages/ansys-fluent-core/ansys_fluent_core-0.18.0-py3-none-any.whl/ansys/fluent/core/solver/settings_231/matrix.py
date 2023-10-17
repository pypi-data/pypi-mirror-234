#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .r import r as r_cls
from .u import u as u_cls
class matrix(Group):
    """
    'matrix' child.
    """

    fluent_name = "matrix"

    child_names = \
        ['r', 'u']

    r: r_cls = r_cls
    """
    r child of matrix.
    """
    u: u_cls = u_cls
    """
    u child of matrix.
    """
