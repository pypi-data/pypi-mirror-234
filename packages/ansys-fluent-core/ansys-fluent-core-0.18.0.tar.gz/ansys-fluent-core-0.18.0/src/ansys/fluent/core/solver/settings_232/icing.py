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
from .icing_child import icing_child

class icing(NamedObject[icing_child], _CreatableNamedObjectMixin[icing_child]):
    """
    'icing' child.
    """

    fluent_name = "icing"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list_cls = list_cls
    """
    list command of icing.
    """
    list_properties: list_properties_cls = list_properties_cls
    """
    list_properties command of icing.
    """
    duplicate: duplicate_cls = duplicate_cls
    """
    duplicate command of icing.
    """
    child_object_type: icing_child = icing_child
    """
    child_object_type of icing.
    """
