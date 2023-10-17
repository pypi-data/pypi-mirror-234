#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .axis_from import axis_from as axis_from_cls
from .axis_to import axis_to as axis_to_cls
class first_axis(Group):
    """
    'first_axis' child.
    """

    fluent_name = "first-axis"

    child_names = \
        ['axis_from', 'axis_to']

    axis_from: axis_from_cls = axis_from_cls
    """
    axis_from child of first_axis.
    """
    axis_to: axis_to_cls = axis_to_cls
    """
    axis_to child of first_axis.
    """
