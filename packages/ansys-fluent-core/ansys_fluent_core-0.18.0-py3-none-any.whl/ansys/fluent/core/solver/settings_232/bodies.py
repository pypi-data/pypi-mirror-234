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
from .bodies_child import bodies_child

class bodies(NamedObject[bodies_child], _CreatableNamedObjectMixin[bodies_child]):
    """
    'bodies' child.
    """

    fluent_name = "bodies"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list_cls = list_cls
    """
    list command of bodies.
    """
    list_properties: list_properties_cls = list_properties_cls
    """
    list_properties command of bodies.
    """
    duplicate: duplicate_cls = duplicate_cls
    """
    duplicate command of bodies.
    """
    child_object_type: bodies_child = bodies_child
    """
    child_object_type of bodies.
    """
