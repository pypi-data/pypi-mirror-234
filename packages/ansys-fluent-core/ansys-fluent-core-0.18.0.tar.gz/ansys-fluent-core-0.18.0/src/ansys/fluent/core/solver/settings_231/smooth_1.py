#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .smooth_partitioning import smooth_partitioning as smooth_partitioning_cls
from .max_smoothing_iterations import max_smoothing_iterations as max_smoothing_iterations_cls
class smooth(Group):
    """
    Set partition smoothing optimization.
    """

    fluent_name = "smooth"

    child_names = \
        ['smooth_partitioning', 'max_smoothing_iterations']

    smooth_partitioning: smooth_partitioning_cls = smooth_partitioning_cls
    """
    smooth_partitioning child of smooth.
    """
    max_smoothing_iterations: max_smoothing_iterations_cls = max_smoothing_iterations_cls
    """
    max_smoothing_iterations child of smooth.
    """
