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
from .user_defined_child import user_defined_child

class user_defined(NamedObject[user_defined_child], _CreatableNamedObjectMixin[user_defined_child]):
    """
    'user_defined' child.
    """

    fluent_name = "user-defined"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list_cls = list_cls
    """
    list command of user_defined.
    """
    list_properties: list_properties_cls = list_properties_cls
    """
    list_properties command of user_defined.
    """
    duplicate: duplicate_cls = duplicate_cls
    """
    duplicate command of user_defined.
    """
    child_object_type: user_defined_child = user_defined_child
    """
    child_object_type of user_defined.
    """
