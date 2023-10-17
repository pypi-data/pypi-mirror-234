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
from .named_expressions_child import named_expressions_child

class named_expressions(NamedObject[named_expressions_child], _CreatableNamedObjectMixin[named_expressions_child]):
    """
    'named_expressions' child.
    """

    fluent_name = "named-expressions"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list_cls = list_cls
    """
    list command of named_expressions.
    """
    list_properties: list_properties_cls = list_properties_cls
    """
    list_properties command of named_expressions.
    """
    duplicate: duplicate_cls = duplicate_cls
    """
    duplicate command of named_expressions.
    """
    child_object_type: named_expressions_child = named_expressions_child
    """
    child_object_type of named_expressions.
    """
