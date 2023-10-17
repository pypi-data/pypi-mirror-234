#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .east_x import east_x as east_x_cls
from .east_y import east_y as east_y_cls
from .east_z import east_z as east_z_cls
class east_direction(Group):
    """
    'east_direction' child.
    """

    fluent_name = "east-direction"

    child_names = \
        ['east_x', 'east_y', 'east_z']

    east_x: east_x_cls = east_x_cls
    """
    east_x child of east_direction.
    """
    east_y: east_y_cls = east_y_cls
    """
    east_y child of east_direction.
    """
    east_z: east_z_cls = east_z_cls
    """
    east_z child of east_direction.
    """
