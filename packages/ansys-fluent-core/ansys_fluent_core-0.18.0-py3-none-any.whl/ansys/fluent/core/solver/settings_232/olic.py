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
from .display_2 import display as display_cls
from .copy_4 import copy as copy_cls
from .add_to_graphics import add_to_graphics as add_to_graphics_cls
from .clear_history import clear_history as clear_history_cls
from .olic_child import olic_child

class olic(NamedObject[olic_child], _CreatableNamedObjectMixin[olic_child]):
    """
    'olic' child.
    """

    fluent_name = "olic"

    command_names = \
        ['list', 'list_properties', 'duplicate', 'display', 'copy',
         'add_to_graphics', 'clear_history']

    list: list_cls = list_cls
    """
    list command of olic.
    """
    list_properties: list_properties_cls = list_properties_cls
    """
    list_properties command of olic.
    """
    duplicate: duplicate_cls = duplicate_cls
    """
    duplicate command of olic.
    """
    display: display_cls = display_cls
    """
    display command of olic.
    """
    copy: copy_cls = copy_cls
    """
    copy command of olic.
    """
    add_to_graphics: add_to_graphics_cls = add_to_graphics_cls
    """
    add_to_graphics command of olic.
    """
    clear_history: clear_history_cls = clear_history_cls
    """
    clear_history command of olic.
    """
    child_object_type: olic_child = olic_child
    """
    child_object_type of olic.
    """
