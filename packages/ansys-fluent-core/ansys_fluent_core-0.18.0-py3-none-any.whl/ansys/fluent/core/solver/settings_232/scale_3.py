#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .border_2 import border as border_cls
from .bottom_2 import bottom as bottom_cls
from .clear_2 import clear as clear_cls
from .format_1 import format as format_cls
from .font_size_1 import font_size as font_size_cls
from .left_2 import left as left_cls
from .margin import margin as margin_cls
from .right_3 import right as right_cls
from .top_2 import top as top_cls
from .visible_3 import visible as visible_cls
class scale(Group):
    """
    Enter the color scale window options menu.
    """

    fluent_name = "scale"

    child_names = \
        ['border', 'bottom', 'clear', 'format', 'font_size', 'left', 'margin',
         'right', 'top', 'visible']

    border: border_cls = border_cls
    """
    border child of scale.
    """
    bottom: bottom_cls = bottom_cls
    """
    bottom child of scale.
    """
    clear: clear_cls = clear_cls
    """
    clear child of scale.
    """
    format: format_cls = format_cls
    """
    format child of scale.
    """
    font_size: font_size_cls = font_size_cls
    """
    font_size child of scale.
    """
    left: left_cls = left_cls
    """
    left child of scale.
    """
    margin: margin_cls = margin_cls
    """
    margin child of scale.
    """
    right: right_cls = right_cls
    """
    right child of scale.
    """
    top: top_cls = top_cls
    """
    top child of scale.
    """
    visible: visible_cls = visible_cls
    """
    visible child of scale.
    """
