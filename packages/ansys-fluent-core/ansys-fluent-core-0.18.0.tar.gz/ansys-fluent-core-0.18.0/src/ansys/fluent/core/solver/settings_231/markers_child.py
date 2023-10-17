#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .symbol import symbol as symbol_cls
from .size_1 import size as size_cls
from .color import color as color_cls
class markers_child(Group):
    """
    'child_object_type' of markers.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['symbol', 'size', 'color']

    symbol: symbol_cls = symbol_cls
    """
    symbol child of markers_child.
    """
    size: size_cls = size_cls
    """
    size child of markers_child.
    """
    color: color_cls = color_cls
    """
    color child of markers_child.
    """
