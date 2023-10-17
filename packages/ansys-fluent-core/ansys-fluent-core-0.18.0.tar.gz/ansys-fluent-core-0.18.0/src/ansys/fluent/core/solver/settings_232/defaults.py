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
from .defaults_child import defaults_child

class defaults(NamedObject[defaults_child], _NonCreatableNamedObjectMixin[defaults_child]):
    """
    'defaults' child.
    """

    fluent_name = "defaults"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list_cls = list_cls
    """
    list command of defaults.
    """
    list_properties: list_properties_cls = list_properties_cls
    """
    list_properties command of defaults.
    """
    duplicate: duplicate_cls = duplicate_cls
    """
    duplicate command of defaults.
    """
    child_object_type: defaults_child = defaults_child
    """
    child_object_type of defaults.
    """
