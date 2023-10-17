#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .option import option as option_cls
from .cell_distance import cell_distance as cell_distance_cls
from .normal_distance import normal_distance as normal_distance_cls
from .volume_distance import volume_distance as volume_distance_cls
class distance_option(Group):
    """
    'distance_option' child.
    """

    fluent_name = "distance-option"

    child_names = \
        ['option', 'cell_distance', 'normal_distance', 'volume_distance']

    option: option_cls = option_cls
    """
    option child of distance_option.
    """
    cell_distance: cell_distance_cls = cell_distance_cls
    """
    cell_distance child of distance_option.
    """
    normal_distance: normal_distance_cls = normal_distance_cls
    """
    normal_distance child of distance_option.
    """
    volume_distance: volume_distance_cls = volume_distance_cls
    """
    volume_distance child of distance_option.
    """
