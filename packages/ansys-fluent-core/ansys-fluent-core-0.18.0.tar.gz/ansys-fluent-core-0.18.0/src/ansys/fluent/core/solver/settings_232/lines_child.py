#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .pattern import pattern as pattern_cls
from .weight import weight as weight_cls
from .color import color as color_cls
class lines_child(Group):
    """
    'child_object_type' of lines.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['pattern', 'weight', 'color']

    pattern: pattern_cls = pattern_cls
    """
    pattern child of lines_child.
    """
    weight: weight_cls = weight_cls
    """
    weight child of lines_child.
    """
    color: color_cls = color_cls
    """
    color child of lines_child.
    """
