#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .enforce_laplace_coarsening import enforce_laplace_coarsening as enforce_laplace_coarsening_cls
from .increase_pre_sweeps import increase_pre_sweeps as increase_pre_sweeps_cls
from .pre_sweeps_3 import pre_sweeps as pre_sweeps_cls
from .specify_coarsening_rate import specify_coarsening_rate as specify_coarsening_rate_cls
from .coarsen_rate import coarsen_rate as coarsen_rate_cls
class amg(Group):
    """
    'amg' child.
    """

    fluent_name = "amg"

    child_names = \
        ['enforce_laplace_coarsening', 'increase_pre_sweeps', 'pre_sweeps',
         'specify_coarsening_rate', 'coarsen_rate']

    enforce_laplace_coarsening: enforce_laplace_coarsening_cls = enforce_laplace_coarsening_cls
    """
    enforce_laplace_coarsening child of amg.
    """
    increase_pre_sweeps: increase_pre_sweeps_cls = increase_pre_sweeps_cls
    """
    increase_pre_sweeps child of amg.
    """
    pre_sweeps: pre_sweeps_cls = pre_sweeps_cls
    """
    pre_sweeps child of amg.
    """
    specify_coarsening_rate: specify_coarsening_rate_cls = specify_coarsening_rate_cls
    """
    specify_coarsening_rate child of amg.
    """
    coarsen_rate: coarsen_rate_cls = coarsen_rate_cls
    """
    coarsen_rate child of amg.
    """
