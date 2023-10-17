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
from .use_active import use_active as use_active_cls
from .restore_state import restore_state as restore_state_cls
from .copy_5 import copy as copy_cls
from .read_3 import read as read_cls
from .write_1 import write as write_cls
from .display_states_child import display_states_child

class display_states(NamedObject[display_states_child], _CreatableNamedObjectMixin[display_states_child]):
    """
    'display_states' child.
    """

    fluent_name = "display-states"

    command_names = \
        ['list', 'list_properties', 'duplicate', 'use_active',
         'restore_state', 'copy', 'read', 'write']

    list: list_cls = list_cls
    """
    list command of display_states.
    """
    list_properties: list_properties_cls = list_properties_cls
    """
    list_properties command of display_states.
    """
    duplicate: duplicate_cls = duplicate_cls
    """
    duplicate command of display_states.
    """
    use_active: use_active_cls = use_active_cls
    """
    use_active command of display_states.
    """
    restore_state: restore_state_cls = restore_state_cls
    """
    restore_state command of display_states.
    """
    copy: copy_cls = copy_cls
    """
    copy command of display_states.
    """
    read: read_cls = read_cls
    """
    read command of display_states.
    """
    write: write_cls = write_cls
    """
    write command of display_states.
    """
    child_object_type: display_states_child = display_states_child
    """
    child_object_type of display_states.
    """
