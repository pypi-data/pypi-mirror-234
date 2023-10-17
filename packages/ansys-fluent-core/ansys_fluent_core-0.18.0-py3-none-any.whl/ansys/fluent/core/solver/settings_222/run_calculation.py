#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .adaptive_time_stepping import adaptive_time_stepping as adaptive_time_stepping_cls
from .cfl_based_adaptive_time_stepping import cfl_based_adaptive_time_stepping as cfl_based_adaptive_time_stepping_cls
from .data_sampling_1 import data_sampling as data_sampling_cls
from .transient_controls import transient_controls as transient_controls_cls
from .dual_time_iterate import dual_time_iterate as dual_time_iterate_cls
from .iterate import iterate as iterate_cls
class run_calculation(Group):
    """
    'run_calculation' child.
    """

    fluent_name = "run-calculation"

    child_names = \
        ['adaptive_time_stepping', 'cfl_based_adaptive_time_stepping',
         'data_sampling', 'transient_controls']

    adaptive_time_stepping: adaptive_time_stepping_cls = adaptive_time_stepping_cls
    """
    adaptive_time_stepping child of run_calculation.
    """
    cfl_based_adaptive_time_stepping: cfl_based_adaptive_time_stepping_cls = cfl_based_adaptive_time_stepping_cls
    """
    cfl_based_adaptive_time_stepping child of run_calculation.
    """
    data_sampling: data_sampling_cls = data_sampling_cls
    """
    data_sampling child of run_calculation.
    """
    transient_controls: transient_controls_cls = transient_controls_cls
    """
    transient_controls child of run_calculation.
    """
    command_names = \
        ['dual_time_iterate', 'iterate']

    dual_time_iterate: dual_time_iterate_cls = dual_time_iterate_cls
    """
    dual_time_iterate command of run_calculation.
    """
    iterate: iterate_cls = iterate_cls
    """
    iterate command of run_calculation.
    """
