#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .residual_smoothing_factor import residual_smoothing_factor as residual_smoothing_factor_cls
from .residual_smoothing_iteration import residual_smoothing_iteration as residual_smoothing_iteration_cls
class residual_smoothing(Group):
    """
    'residual_smoothing' child.
    """

    fluent_name = "residual-smoothing"

    child_names = \
        ['residual_smoothing_factor', 'residual_smoothing_iteration']

    residual_smoothing_factor: residual_smoothing_factor_cls = residual_smoothing_factor_cls
    """
    residual_smoothing_factor child of residual_smoothing.
    """
    residual_smoothing_iteration: residual_smoothing_iteration_cls = residual_smoothing_iteration_cls
    """
    residual_smoothing_iteration child of residual_smoothing.
    """
