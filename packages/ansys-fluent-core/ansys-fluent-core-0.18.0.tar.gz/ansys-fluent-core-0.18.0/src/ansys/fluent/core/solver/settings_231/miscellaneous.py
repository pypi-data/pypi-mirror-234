#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .compute_statistics import compute_statistics as compute_statistics_cls
from .statistics_level import statistics_level as statistics_level_cls
class miscellaneous(Group):
    """
    'miscellaneous' child.
    """

    fluent_name = "miscellaneous"

    child_names = \
        ['compute_statistics', 'statistics_level']

    compute_statistics: compute_statistics_cls = compute_statistics_cls
    """
    compute_statistics child of miscellaneous.
    """
    statistics_level: statistics_level_cls = statistics_level_cls
    """
    statistics_level child of miscellaneous.
    """
