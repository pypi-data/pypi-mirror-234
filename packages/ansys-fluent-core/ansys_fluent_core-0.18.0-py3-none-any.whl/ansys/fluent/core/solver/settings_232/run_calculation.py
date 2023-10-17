#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .pseudo_time_settings import pseudo_time_settings as pseudo_time_settings_cls
from .iter_count_2 import iter_count as iter_count_cls
from .adaptive_time_stepping import adaptive_time_stepping as adaptive_time_stepping_cls
from .cfl_based_adaptive_time_stepping import cfl_based_adaptive_time_stepping as cfl_based_adaptive_time_stepping_cls
from .reporting_interval import reporting_interval as reporting_interval_cls
from .time_step_count_1 import time_step_count as time_step_count_cls
from .transient_controls import transient_controls as transient_controls_cls
from .data_sampling_1 import data_sampling as data_sampling_cls
from .data_sampling_options import data_sampling_options as data_sampling_options_cls
from .residual_verbosity import residual_verbosity as residual_verbosity_cls
from .calculate import calculate as calculate_cls
from .interrupt import interrupt as interrupt_cls
from .dual_time_iterate import dual_time_iterate as dual_time_iterate_cls
from .iterate import iterate as iterate_cls
from .iterating import iterating as iterating_cls
class run_calculation(Group):
    """
    'run_calculation' child.
    """

    fluent_name = "run-calculation"

    child_names = \
        ['pseudo_time_settings', 'iter_count', 'adaptive_time_stepping',
         'cfl_based_adaptive_time_stepping', 'reporting_interval',
         'time_step_count', 'transient_controls', 'data_sampling',
         'data_sampling_options', 'residual_verbosity']

    pseudo_time_settings: pseudo_time_settings_cls = pseudo_time_settings_cls
    """
    pseudo_time_settings child of run_calculation.
    """
    iter_count: iter_count_cls = iter_count_cls
    """
    iter_count child of run_calculation.
    """
    adaptive_time_stepping: adaptive_time_stepping_cls = adaptive_time_stepping_cls
    """
    adaptive_time_stepping child of run_calculation.
    """
    cfl_based_adaptive_time_stepping: cfl_based_adaptive_time_stepping_cls = cfl_based_adaptive_time_stepping_cls
    """
    cfl_based_adaptive_time_stepping child of run_calculation.
    """
    reporting_interval: reporting_interval_cls = reporting_interval_cls
    """
    reporting_interval child of run_calculation.
    """
    time_step_count: time_step_count_cls = time_step_count_cls
    """
    time_step_count child of run_calculation.
    """
    transient_controls: transient_controls_cls = transient_controls_cls
    """
    transient_controls child of run_calculation.
    """
    data_sampling: data_sampling_cls = data_sampling_cls
    """
    data_sampling child of run_calculation.
    """
    data_sampling_options: data_sampling_options_cls = data_sampling_options_cls
    """
    data_sampling_options child of run_calculation.
    """
    residual_verbosity: residual_verbosity_cls = residual_verbosity_cls
    """
    residual_verbosity child of run_calculation.
    """
    command_names = \
        ['calculate', 'interrupt', 'dual_time_iterate', 'iterate']

    calculate: calculate_cls = calculate_cls
    """
    calculate command of run_calculation.
    """
    interrupt: interrupt_cls = interrupt_cls
    """
    interrupt command of run_calculation.
    """
    dual_time_iterate: dual_time_iterate_cls = dual_time_iterate_cls
    """
    dual_time_iterate command of run_calculation.
    """
    iterate: iterate_cls = iterate_cls
    """
    iterate command of run_calculation.
    """
    query_names = \
        ['iterating']

    iterating: iterating_cls = iterating_cls
    """
    iterating query of run_calculation.
    """
