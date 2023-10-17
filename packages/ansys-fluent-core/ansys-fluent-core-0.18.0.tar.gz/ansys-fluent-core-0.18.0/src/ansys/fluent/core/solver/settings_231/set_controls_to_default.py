#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .solution_controls import solution_controls as solution_controls_cls
from .amg_controls_1 import amg_controls as amg_controls_cls
from .multi_stage_parameter import multi_stage_parameter as multi_stage_parameter_cls
from .limits_1 import limits as limits_cls
from .reset_pseudo_time_method_generic import reset_pseudo_time_method_generic as reset_pseudo_time_method_generic_cls
from .reset_pseudo_time_method_equations import reset_pseudo_time_method_equations as reset_pseudo_time_method_equations_cls
from .reset_pseudo_time_method_relaxations import reset_pseudo_time_method_relaxations as reset_pseudo_time_method_relaxations_cls
from .reset_pseudo_time_method_scale_factors import reset_pseudo_time_method_scale_factors as reset_pseudo_time_method_scale_factors_cls
class set_controls_to_default(Group):
    """
    'set_controls_to_default' child.
    """

    fluent_name = "set-controls-to-default"

    command_names = \
        ['solution_controls', 'amg_controls', 'multi_stage_parameter',
         'limits', 'reset_pseudo_time_method_generic',
         'reset_pseudo_time_method_equations',
         'reset_pseudo_time_method_relaxations',
         'reset_pseudo_time_method_scale_factors']

    solution_controls: solution_controls_cls = solution_controls_cls
    """
    solution_controls command of set_controls_to_default.
    """
    amg_controls: amg_controls_cls = amg_controls_cls
    """
    amg_controls command of set_controls_to_default.
    """
    multi_stage_parameter: multi_stage_parameter_cls = multi_stage_parameter_cls
    """
    multi_stage_parameter command of set_controls_to_default.
    """
    limits: limits_cls = limits_cls
    """
    limits command of set_controls_to_default.
    """
    reset_pseudo_time_method_generic: reset_pseudo_time_method_generic_cls = reset_pseudo_time_method_generic_cls
    """
    reset_pseudo_time_method_generic command of set_controls_to_default.
    """
    reset_pseudo_time_method_equations: reset_pseudo_time_method_equations_cls = reset_pseudo_time_method_equations_cls
    """
    reset_pseudo_time_method_equations command of set_controls_to_default.
    """
    reset_pseudo_time_method_relaxations: reset_pseudo_time_method_relaxations_cls = reset_pseudo_time_method_relaxations_cls
    """
    reset_pseudo_time_method_relaxations command of set_controls_to_default.
    """
    reset_pseudo_time_method_scale_factors: reset_pseudo_time_method_scale_factors_cls = reset_pseudo_time_method_scale_factors_cls
    """
    reset_pseudo_time_method_scale_factors command of set_controls_to_default.
    """
