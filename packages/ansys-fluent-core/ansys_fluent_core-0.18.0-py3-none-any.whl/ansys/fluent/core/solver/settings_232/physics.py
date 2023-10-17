#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .volumes import volumes as volumes_cls
from .interfaces import interfaces as interfaces_cls
from .list_physics import list_physics as list_physics_cls
class physics(Group):
    """
    'physics' child.
    """

    fluent_name = "physics"

    child_names = \
        ['volumes', 'interfaces']

    volumes: volumes_cls = volumes_cls
    """
    volumes child of physics.
    """
    interfaces: interfaces_cls = interfaces_cls
    """
    interfaces child of physics.
    """
    command_names = \
        ['list_physics']

    list_physics: list_physics_cls = list_physics_cls
    """
    list_physics command of physics.
    """
