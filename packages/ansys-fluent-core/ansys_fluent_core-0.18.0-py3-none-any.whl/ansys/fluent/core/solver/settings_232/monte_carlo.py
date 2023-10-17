#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .number_of_histories import number_of_histories as number_of_histories_cls
from .under_relaxation import under_relaxation as under_relaxation_cls
from .target_cells_per_volume_cluster import target_cells_per_volume_cluster as target_cells_per_volume_cluster_cls
class monte_carlo(Group):
    """
    Enable/disable the Monte Carlo radiation model.
    """

    fluent_name = "monte-carlo"

    child_names = \
        ['number_of_histories', 'under_relaxation',
         'target_cells_per_volume_cluster']

    number_of_histories: number_of_histories_cls = number_of_histories_cls
    """
    number_of_histories child of monte_carlo.
    """
    under_relaxation: under_relaxation_cls = under_relaxation_cls
    """
    under_relaxation child of monte_carlo.
    """
    target_cells_per_volume_cluster: target_cells_per_volume_cluster_cls = target_cells_per_volume_cluster_cls
    """
    target_cells_per_volume_cluster child of monte_carlo.
    """
