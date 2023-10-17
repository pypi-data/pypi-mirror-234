#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .border_1 import border as border_cls
from .bottom_1 import bottom as bottom_cls
from .left_1 import left as left_cls
from .right_2 import right as right_cls
from .top_1 import top as top_cls
from .visible_2 import visible as visible_cls
class main(Group):
    """
    Enter the main view window options menu.
    """

    fluent_name = "main"

    child_names = \
        ['border', 'bottom', 'left', 'right', 'top', 'visible']

    border: border_cls = border_cls
    """
    border child of main.
    """
    bottom: bottom_cls = bottom_cls
    """
    bottom child of main.
    """
    left: left_cls = left_cls
    """
    left child of main.
    """
    right: right_cls = right_cls
    """
    right child of main.
    """
    top: top_cls = top_cls
    """
    top child of main.
    """
    visible: visible_cls = visible_cls
    """
    visible child of main.
    """
