#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .smoothed_density_stabilization_method import smoothed_density_stabilization_method as smoothed_density_stabilization_method_cls
from .num_of_density_smoothing import num_of_density_smoothing as num_of_density_smoothing_cls
from .false_time_step_linearization import false_time_step_linearization as false_time_step_linearization_cls
from .auto_dt_advanced_controls import auto_dt_advanced_controls as auto_dt_advanced_controls_cls
class pseudo_transient(Group):
    """
    'pseudo_transient' child.
    """

    fluent_name = "pseudo-transient"

    child_names = \
        ['smoothed_density_stabilization_method', 'num_of_density_smoothing',
         'false_time_step_linearization', 'auto_dt_advanced_controls']

    smoothed_density_stabilization_method: smoothed_density_stabilization_method_cls = smoothed_density_stabilization_method_cls
    """
    smoothed_density_stabilization_method child of pseudo_transient.
    """
    num_of_density_smoothing: num_of_density_smoothing_cls = num_of_density_smoothing_cls
    """
    num_of_density_smoothing child of pseudo_transient.
    """
    false_time_step_linearization: false_time_step_linearization_cls = false_time_step_linearization_cls
    """
    false_time_step_linearization child of pseudo_transient.
    """
    auto_dt_advanced_controls: auto_dt_advanced_controls_cls = auto_dt_advanced_controls_cls
    """
    auto_dt_advanced_controls child of pseudo_transient.
    """
