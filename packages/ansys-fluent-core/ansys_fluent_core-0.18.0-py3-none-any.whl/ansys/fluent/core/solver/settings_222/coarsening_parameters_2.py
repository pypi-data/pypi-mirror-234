#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .max_coarse_levels_2 import max_coarse_levels as max_coarse_levels_cls
from .coarsen_by_interval_2 import coarsen_by_interval as coarsen_by_interval_cls
class coarsening_parameters(Group):
    """
    'coarsening_parameters' child.
    """

    fluent_name = "coarsening-parameters"

    child_names = \
        ['max_coarse_levels', 'coarsen_by_interval']

    max_coarse_levels: max_coarse_levels_cls = max_coarse_levels_cls
    """
    max_coarse_levels child of coarsening_parameters.
    """
    coarsen_by_interval: coarsen_by_interval_cls = coarsen_by_interval_cls
    """
    coarsen_by_interval child of coarsening_parameters.
    """
