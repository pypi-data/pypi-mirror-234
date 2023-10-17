#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .total_period_count import total_period_count as total_period_count_cls
from .time_step_count_2 import time_step_count as time_step_count_cls
from .total_time_step_count import total_time_step_count as total_time_step_count_cls
from .total_time import total_time as total_time_cls
from .incremental_time import incremental_time as incremental_time_cls
from .max_iter_per_step import max_iter_per_step as max_iter_per_step_cls
from .postprocess import postprocess as postprocess_cls
from .post_iter_per_time_step_count import post_iter_per_time_step_count as post_iter_per_time_step_count_cls
class dual_time_iterate(Command):
    """
    Perform unsteady iterations.
    
    Parameters
    ----------
        total_period_count : int
            Set number of total periods.
        time_step_count : int
            Set inceremtal number of Time steps.
        total_time_step_count : int
            Set total number of Time steps.
        total_time : real
            Set Total Simulation Time.
        incremental_time : real
            Set Incremental Time.
        max_iter_per_step : int
            Set Maximum Number of iterations per time step.
        postprocess : bool
            Enable/Disable Postprocess pollutant solution?.
        post_iter_per_time_step_count : int
            Set Number of post-processing iterations per time step.
    
    """

    fluent_name = "dual-time-iterate"

    argument_names = \
        ['total_period_count', 'time_step_count', 'total_time_step_count',
         'total_time', 'incremental_time', 'max_iter_per_step', 'postprocess',
         'post_iter_per_time_step_count']

    total_period_count: total_period_count_cls = total_period_count_cls
    """
    total_period_count argument of dual_time_iterate.
    """
    time_step_count: time_step_count_cls = time_step_count_cls
    """
    time_step_count argument of dual_time_iterate.
    """
    total_time_step_count: total_time_step_count_cls = total_time_step_count_cls
    """
    total_time_step_count argument of dual_time_iterate.
    """
    total_time: total_time_cls = total_time_cls
    """
    total_time argument of dual_time_iterate.
    """
    incremental_time: incremental_time_cls = incremental_time_cls
    """
    incremental_time argument of dual_time_iterate.
    """
    max_iter_per_step: max_iter_per_step_cls = max_iter_per_step_cls
    """
    max_iter_per_step argument of dual_time_iterate.
    """
    postprocess: postprocess_cls = postprocess_cls
    """
    postprocess argument of dual_time_iterate.
    """
    post_iter_per_time_step_count: post_iter_per_time_step_count_cls = post_iter_per_time_step_count_cls
    """
    post_iter_per_time_step_count argument of dual_time_iterate.
    """
