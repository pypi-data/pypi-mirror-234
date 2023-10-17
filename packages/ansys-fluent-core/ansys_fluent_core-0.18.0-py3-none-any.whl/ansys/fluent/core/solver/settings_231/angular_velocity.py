#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .x import x as x_cls
from .x_2 import x_2 as x_2_cls
from .y import y as y_cls
from .y_2 import y_2 as y_2_cls
from .z import z as z_cls
from .z_2 import z_2 as z_2_cls
from .magnitude import magnitude as magnitude_cls
class angular_velocity(Group):
    """
    'angular_velocity' child.
    """

    fluent_name = "angular-velocity"

    child_names = \
        ['x', 'x_2', 'y', 'y_2', 'z', 'z_2', 'magnitude']

    x: x_cls = x_cls
    """
    x child of angular_velocity.
    """
    x_2: x_2_cls = x_2_cls
    """
    x_2 child of angular_velocity.
    """
    y: y_cls = y_cls
    """
    y child of angular_velocity.
    """
    y_2: y_2_cls = y_2_cls
    """
    y_2 child of angular_velocity.
    """
    z: z_cls = z_cls
    """
    z child of angular_velocity.
    """
    z_2: z_2_cls = z_2_cls
    """
    z_2 child of angular_velocity.
    """
    magnitude: magnitude_cls = magnitude_cls
    """
    magnitude child of angular_velocity.
    """
