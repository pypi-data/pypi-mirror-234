#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .x_axis_1 import x_axis as x_axis_cls
from .y_axis_1 import y_axis as y_axis_cls
class rules(Group):
    """
    'rules' child.
    """

    fluent_name = "rules"

    child_names = \
        ['x_axis', 'y_axis']

    x_axis: x_axis_cls = x_axis_cls
    """
    x_axis child of rules.
    """
    y_axis: y_axis_cls = y_axis_cls
    """
    y_axis child of rules.
    """
