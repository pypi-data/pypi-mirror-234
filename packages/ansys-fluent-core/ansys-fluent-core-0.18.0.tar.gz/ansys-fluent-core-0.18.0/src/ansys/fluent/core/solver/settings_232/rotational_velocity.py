#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .speed import speed as speed_cls
from .rotation_axis import rotation_axis as rotation_axis_cls
class rotational_velocity(Group):
    """
    'rotational_velocity' child.
    """

    fluent_name = "rotational-velocity"

    child_names = \
        ['speed', 'rotation_axis']

    speed: speed_cls = speed_cls
    """
    speed child of rotational_velocity.
    """
    rotation_axis: rotation_axis_cls = rotation_axis_cls
    """
    rotation_axis child of rotational_velocity.
    """
