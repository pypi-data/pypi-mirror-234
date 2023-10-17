#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .enabled_2 import enabled as enabled_cls
from .color import color as color_cls
class constant_color(Group):
    """
    'constant_color' child.
    """

    fluent_name = "constant-color"

    child_names = \
        ['enabled', 'color']

    enabled: enabled_cls = enabled_cls
    """
    enabled child of constant_color.
    """
    color: color_cls = color_cls
    """
    color child of constant_color.
    """
