#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .option_2 import option as option_cls
from .auto_range import auto_range as auto_range_cls
from .clip_to_range_1 import clip_to_range as clip_to_range_cls
class range(Group):
    """
    'range' child.
    """

    fluent_name = "range"

    child_names = \
        ['option', 'auto_range', 'clip_to_range']

    option: option_cls = option_cls
    """
    option child of range.
    """
    auto_range: auto_range_cls = auto_range_cls
    """
    auto_range child of range.
    """
    clip_to_range: clip_to_range_cls = clip_to_range_cls
    """
    clip_to_range child of range.
    """
