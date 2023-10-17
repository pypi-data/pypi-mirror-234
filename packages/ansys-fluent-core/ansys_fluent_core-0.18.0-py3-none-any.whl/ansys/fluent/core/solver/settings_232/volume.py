#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .list import list as list_cls
from .list_properties import list_properties as list_properties_cls
from .duplicate import duplicate as duplicate_cls
from .volume_child import volume_child

class volume(NamedObject[volume_child], _CreatableNamedObjectMixin[volume_child]):
    """
    'volume' child.
    """

    fluent_name = "volume"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list_cls = list_cls
    """
    list command of volume.
    """
    list_properties: list_properties_cls = list_properties_cls
    """
    list_properties command of volume.
    """
    duplicate: duplicate_cls = duplicate_cls
    """
    duplicate command of volume.
    """
    child_object_type: volume_child = volume_child
    """
    child_object_type of volume.
    """
