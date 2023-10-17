#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .direction_option import direction_option as direction_option_cls
from .vector import vector as vector_cls
from .point import point as point_cls
from .axis_label import axis_label as axis_label_cls
class axis_from(Group):
    """
    'axis_from' child.
    """

    fluent_name = "axis-from"

    child_names = \
        ['direction_option', 'vector', 'point', 'axis_label']

    direction_option: direction_option_cls = direction_option_cls
    """
    direction_option child of axis_from.
    """
    vector: vector_cls = vector_cls
    """
    vector child of axis_from.
    """
    point: point_cls = point_cls
    """
    point child of axis_from.
    """
    axis_label: axis_label_cls = axis_label_cls
    """
    axis_label child of axis_from.
    """
