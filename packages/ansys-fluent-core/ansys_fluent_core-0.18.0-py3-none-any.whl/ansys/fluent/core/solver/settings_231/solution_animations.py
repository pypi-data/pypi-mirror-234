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
from .solution_animations_child import solution_animations_child

class solution_animations(NamedObject[solution_animations_child], _CreatableNamedObjectMixin[solution_animations_child]):
    """
    'solution_animations' child.
    """

    fluent_name = "solution-animations"

    command_names = \
        ['display', 'copy', 'add_to_graphics', 'clear_history']

    display: display_cls = display_cls
    """
    display command of solution_animations.
    """
    copy: copy_cls = copy_cls
    """
    copy command of solution_animations.
    """
    add_to_graphics: add_to_graphics_cls = add_to_graphics_cls
    """
    add_to_graphics command of solution_animations.
    """
    clear_history: clear_history_cls = clear_history_cls
    """
    clear_history command of solution_animations.
    """
    child_object_type: solution_animations_child = solution_animations_child
    """
    child_object_type of solution_animations.
    """
