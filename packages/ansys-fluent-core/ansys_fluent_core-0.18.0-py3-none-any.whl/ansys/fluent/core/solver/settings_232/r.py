#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .x import x as x_cls
from .y import y as y_cls
from .z import z as z_cls
class r(Group):
    """
    'r' child.
    """

    fluent_name = "r"

    child_names = \
        ['x', 'y', 'z']

    x: x_cls = x_cls
    """
    x child of r.
    """
    y: y_cls = y_cls
    """
    y child of r.
    """
    z: z_cls = z_cls
    """
    z child of r.
    """
