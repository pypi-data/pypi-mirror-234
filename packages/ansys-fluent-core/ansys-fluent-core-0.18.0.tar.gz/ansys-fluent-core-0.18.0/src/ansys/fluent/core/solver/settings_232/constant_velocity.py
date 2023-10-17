#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .linear_velocity import linear_velocity as linear_velocity_cls
from .rotational_velocity import rotational_velocity as rotational_velocity_cls
class constant_velocity(Group):
    """
    'constant_velocity' child.
    """

    fluent_name = "constant-velocity"

    child_names = \
        ['linear_velocity', 'rotational_velocity']

    linear_velocity: linear_velocity_cls = linear_velocity_cls
    """
    linear_velocity child of constant_velocity.
    """
    rotational_velocity: rotational_velocity_cls = rotational_velocity_cls
    """
    rotational_velocity child of constant_velocity.
    """
