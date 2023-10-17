#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .clip_to_range import clip_to_range as clip_to_range_cls
from .minimum import minimum as minimum_cls
from .maximum import maximum as maximum_cls
class auto_range_off(Group):
    """
    'auto_range_off' child.
    """

    fluent_name = "auto-range-off"

    child_names = \
        ['clip_to_range', 'minimum', 'maximum']

    clip_to_range: clip_to_range_cls = clip_to_range_cls
    """
    clip_to_range child of auto_range_off.
    """
    minimum: minimum_cls = minimum_cls
    """
    minimum child of auto_range_off.
    """
    maximum: maximum_cls = maximum_cls
    """
    maximum child of auto_range_off.
    """
