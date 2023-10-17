#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .subspace_size import subspace_size as subspace_size_cls
from .skip_iter_count import skip_iter_count as skip_iter_count_cls
class reduced_rank_extrapolation_options(Group):
    """
    Reduced Rank Extrapolation options.
    """

    fluent_name = "reduced-rank-extrapolation-options"

    child_names = \
        ['subspace_size', 'skip_iter_count']

    subspace_size: subspace_size_cls = subspace_size_cls
    """
    subspace_size child of reduced_rank_extrapolation_options.
    """
    skip_iter_count: skip_iter_count_cls = skip_iter_count_cls
    """
    skip_iter_count child of reduced_rank_extrapolation_options.
    """
