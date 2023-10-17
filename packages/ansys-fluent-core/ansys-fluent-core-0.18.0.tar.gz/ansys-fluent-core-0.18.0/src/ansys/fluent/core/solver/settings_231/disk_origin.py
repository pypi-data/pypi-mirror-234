#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .disk_origin_x import disk_origin_x as disk_origin_x_cls
from .disk_origin_y import disk_origin_y as disk_origin_y_cls
from .disk_origin_z import disk_origin_z as disk_origin_z_cls
class disk_origin(Group):
    """
    Menu to define the disk center coordinates.
    For more details please consult the help option of the corresponding menu or TUI command.
    """

    fluent_name = "disk-origin"

    child_names = \
        ['disk_origin_x', 'disk_origin_y', 'disk_origin_z']

    disk_origin_x: disk_origin_x_cls = disk_origin_x_cls
    """
    disk_origin_x child of disk_origin.
    """
    disk_origin_y: disk_origin_y_cls = disk_origin_y_cls
    """
    disk_origin_y child of disk_origin.
    """
    disk_origin_z: disk_origin_z_cls = disk_origin_z_cls
    """
    disk_origin_z child of disk_origin.
    """
