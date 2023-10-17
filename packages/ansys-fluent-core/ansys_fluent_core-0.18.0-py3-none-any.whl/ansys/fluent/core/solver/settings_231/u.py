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
class u(Group):
    """
    'u' child.
    """

    fluent_name = "u"

    child_names = \
        ['x', 'y', 'z']

    x: x_cls = x_cls
    """
    x child of u.
    """
    y: y_cls = y_cls
    """
    y child of u.
    """
    z: z_cls = z_cls
    """
    z child of u.
    """
