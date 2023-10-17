#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .border_4 import border as border_cls
from .bottom_4 import bottom as bottom_cls
from .left_4 import left as left_cls
from .right_5 import right as right_cls
from .top_4 import top as top_cls
from .visible_5 import visible as visible_cls
class xy(Group):
    """
    Enter the X-Y plot window options menu.
    """

    fluent_name = "xy"

    child_names = \
        ['border', 'bottom', 'left', 'right', 'top', 'visible']

    border: border_cls = border_cls
    """
    border child of xy.
    """
    bottom: bottom_cls = bottom_cls
    """
    bottom child of xy.
    """
    left: left_cls = left_cls
    """
    left child of xy.
    """
    right: right_cls = right_cls
    """
    right child of xy.
    """
    top: top_cls = top_cls
    """
    top child of xy.
    """
    visible: visible_cls = visible_cls
    """
    visible child of xy.
    """
