#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .min_value import min_value as min_value_cls
from .max_value import max_value as max_value_cls
class clip_to_range(Group):
    """
    'clip_to_range' child.
    """

    fluent_name = "clip-to-range"

    child_names = \
        ['min_value', 'max_value']

    min_value: min_value_cls = min_value_cls
    """
    min_value child of clip_to_range.
    """
    max_value: max_value_cls = max_value_cls
    """
    max_value child of clip_to_range.
    """
