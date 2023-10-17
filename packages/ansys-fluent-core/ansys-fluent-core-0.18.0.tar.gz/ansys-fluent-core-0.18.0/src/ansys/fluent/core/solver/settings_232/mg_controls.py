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
from .mg_controls_child import mg_controls_child

class mg_controls(NamedObject[mg_controls_child], _NonCreatableNamedObjectMixin[mg_controls_child]):
    """
    'mg_controls' child.
    """

    fluent_name = "mg-controls"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list_cls = list_cls
    """
    list command of mg_controls.
    """
    list_properties: list_properties_cls = list_properties_cls
    """
    list_properties command of mg_controls.
    """
    duplicate: duplicate_cls = duplicate_cls
    """
    duplicate command of mg_controls.
    """
    child_object_type: mg_controls_child = mg_controls_child
    """
    child_object_type of mg_controls.
    """
