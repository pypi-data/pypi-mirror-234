#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .first_axis import first_axis as first_axis_cls
from .second_axis import second_axis as second_axis_cls
from .auto_second_axis import auto_second_axis as auto_second_axis_cls
class orientation(Group):
    """
    'orientation' child.
    """

    fluent_name = "orientation"

    child_names = \
        ['first_axis', 'second_axis', 'auto_second_axis']

    first_axis: first_axis_cls = first_axis_cls
    """
    first_axis child of orientation.
    """
    second_axis: second_axis_cls = second_axis_cls
    """
    second_axis child of orientation.
    """
    auto_second_axis: auto_second_axis_cls = auto_second_axis_cls
    """
    auto_second_axis child of orientation.
    """
