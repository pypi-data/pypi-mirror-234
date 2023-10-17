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
from .periodic_child import periodic_child

class periodic(NamedObject[periodic_child], _NonCreatableNamedObjectMixin[periodic_child]):
    """
    'periodic' child.
    """

    fluent_name = "periodic"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list_cls = list_cls
    """
    list command of periodic.
    """
    list_properties: list_properties_cls = list_properties_cls
    """
    list_properties command of periodic.
    """
    duplicate: duplicate_cls = duplicate_cls
    """
    duplicate command of periodic.
    """
    child_object_type: periodic_child = periodic_child
    """
    child_object_type of periodic.
    """
