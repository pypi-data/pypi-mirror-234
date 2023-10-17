#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .border import border as border_cls
from .bottom import bottom as bottom_cls
from .clear_1 import clear as clear_cls
from .left import left as left_cls
from .right_1 import right as right_cls
from .top import top as top_cls
from .visible_1 import visible as visible_cls
class axes(Group):
    """
    Enter the axes window options menu.
    """

    fluent_name = "axes"

    child_names = \
        ['border', 'bottom', 'clear', 'left', 'right', 'top', 'visible']

    border: border_cls = border_cls
    """
    border child of axes.
    """
    bottom: bottom_cls = bottom_cls
    """
    bottom child of axes.
    """
    clear: clear_cls = clear_cls
    """
    clear child of axes.
    """
    left: left_cls = left_cls
    """
    left child of axes.
    """
    right: right_cls = right_cls
    """
    right child of axes.
    """
    top: top_cls = top_cls
    """
    top child of axes.
    """
    visible: visible_cls = visible_cls
    """
    visible child of axes.
    """
