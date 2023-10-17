#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .option_13 import option as option_cls
from .min_allowed import min_allowed as min_allowed_cls
from .max_allowed import max_allowed as max_allowed_cls
from .wall_zones import wall_zones as wall_zones_cls
from .phase_26 import phase as phase_cls
class yplus_ystar(Group):
    """
    'yplus_ystar' child.
    """

    fluent_name = "yplus-ystar"

    child_names = \
        ['option', 'min_allowed', 'max_allowed', 'wall_zones', 'phase']

    option: option_cls = option_cls
    """
    option child of yplus_ystar.
    """
    min_allowed: min_allowed_cls = min_allowed_cls
    """
    min_allowed child of yplus_ystar.
    """
    max_allowed: max_allowed_cls = max_allowed_cls
    """
    max_allowed child of yplus_ystar.
    """
    wall_zones: wall_zones_cls = wall_zones_cls
    """
    wall_zones child of yplus_ystar.
    """
    phase: phase_cls = phase_cls
    """
    phase child of yplus_ystar.
    """
