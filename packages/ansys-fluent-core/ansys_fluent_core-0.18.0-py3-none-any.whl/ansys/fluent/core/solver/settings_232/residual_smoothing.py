#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .residual_smoothing_factor import residual_smoothing_factor as residual_smoothing_factor_cls
from .residual_smoothing_iter_count import residual_smoothing_iter_count as residual_smoothing_iter_count_cls
class residual_smoothing(Group):
    """
    Set residual smoothing factor and number of iterations.
    """

    fluent_name = "residual-smoothing"

    child_names = \
        ['residual_smoothing_factor', 'residual_smoothing_iter_count']

    residual_smoothing_factor: residual_smoothing_factor_cls = residual_smoothing_factor_cls
    """
    residual_smoothing_factor child of residual_smoothing.
    """
    residual_smoothing_iter_count: residual_smoothing_iter_count_cls = residual_smoothing_iter_count_cls
    """
    residual_smoothing_iter_count child of residual_smoothing.
    """
