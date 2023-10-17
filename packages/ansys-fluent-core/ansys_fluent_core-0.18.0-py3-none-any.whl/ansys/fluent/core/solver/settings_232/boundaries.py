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
from .boundaries_child import boundaries_child

class boundaries(NamedObject[boundaries_child], _CreatableNamedObjectMixin[boundaries_child]):
    """
    'boundaries' child.
    """

    fluent_name = "boundaries"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list_cls = list_cls
    """
    list command of boundaries.
    """
    list_properties: list_properties_cls = list_properties_cls
    """
    list_properties command of boundaries.
    """
    duplicate: duplicate_cls = duplicate_cls
    """
    duplicate command of boundaries.
    """
    child_object_type: boundaries_child = boundaries_child
    """
    child_object_type of boundaries.
    """
