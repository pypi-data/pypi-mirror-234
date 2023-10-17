#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .display_1 import display as display_cls
from .copy_3 import copy as copy_cls
from .add_to_graphics import add_to_graphics as add_to_graphics_cls
from .clear_history import clear_history as clear_history_cls
from .lic_child import lic_child

class olic(NamedObject[lic_child], _CreatableNamedObjectMixin[lic_child]):
    """
    'olic' child.
    """

    fluent_name = "olic"

    command_names = \
        ['display', 'copy', 'add_to_graphics', 'clear_history']

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
    child_object_type: lic_child = lic_child
    """
    child_object_type of olic.
    """
