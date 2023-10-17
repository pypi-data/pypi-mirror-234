#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .delete import delete as delete_cls
from .display import display as display_cls
from .read_2 import read as read_cls
class surface_mesh(Group):
    """
    Enter the surface mesh menu.
    """

    fluent_name = "surface-mesh"

    command_names = \
        ['delete', 'display', 'read']

    delete: delete_cls = delete_cls
    """
    delete command of surface_mesh.
    """
    display: display_cls = display_cls
    """
    display command of surface_mesh.
    """
    read: read_cls = read_cls
    """
    read command of surface_mesh.
    """
