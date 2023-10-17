#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .option_2 import option as option_cls
from .none_1 import none as none_cls
from .scale_by_global_average import scale_by_global_average as scale_by_global_average_cls
from .scale_by_zone_average import scale_by_zone_average as scale_by_zone_average_cls
from .scale_by_global_maximum import scale_by_global_maximum as scale_by_global_maximum_cls
from .scale_by_zone_maximum import scale_by_zone_maximum as scale_by_zone_maximum_cls
class scaling(Group):
    """
    'scaling' child.
    """

    fluent_name = "scaling"

    child_names = \
        ['option', 'none', 'scale_by_global_average', 'scale_by_zone_average',
         'scale_by_global_maximum', 'scale_by_zone_maximum']

    option: option_cls = option_cls
    """
    option child of scaling.
    """
    none: none_cls = none_cls
    """
    none child of scaling.
    """
    scale_by_global_average: scale_by_global_average_cls = scale_by_global_average_cls
    """
    scale_by_global_average child of scaling.
    """
    scale_by_zone_average: scale_by_zone_average_cls = scale_by_zone_average_cls
    """
    scale_by_zone_average child of scaling.
    """
    scale_by_global_maximum: scale_by_global_maximum_cls = scale_by_global_maximum_cls
    """
    scale_by_global_maximum child of scaling.
    """
    scale_by_zone_maximum: scale_by_zone_maximum_cls = scale_by_zone_maximum_cls
    """
    scale_by_zone_maximum child of scaling.
    """
