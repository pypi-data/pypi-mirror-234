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
from .pressure_far_field_child import pressure_far_field_child

class pressure_far_field(NamedObject[pressure_far_field_child], _NonCreatableNamedObjectMixin[pressure_far_field_child]):
    """
    'pressure_far_field' child.
    """

    fluent_name = "pressure-far-field"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list_cls = list_cls
    """
    list command of pressure_far_field.
    """
    list_properties: list_properties_cls = list_properties_cls
    """
    list_properties command of pressure_far_field.
    """
    duplicate: duplicate_cls = duplicate_cls
    """
    duplicate command of pressure_far_field.
    """
    child_object_type: pressure_far_field_child = pressure_far_field_child
    """
    child_object_type of pressure_far_field.
    """
