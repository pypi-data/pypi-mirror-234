#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .subspace_size import subspace_size as subspace_size_cls
from .skip_itr import skip_itr as skip_itr_cls
class reduced_rank_extrapolation_options(Group):
    """
    'reduced_rank_extrapolation_options' child.
    """

    fluent_name = "reduced-rank-extrapolation-options"

    child_names = \
        ['subspace_size', 'skip_itr']

    subspace_size: subspace_size_cls = subspace_size_cls
    """
    subspace_size child of reduced_rank_extrapolation_options.
    """
    skip_itr: skip_itr_cls = skip_itr_cls
    """
    skip_itr child of reduced_rank_extrapolation_options.
    """
