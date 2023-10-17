#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .method_2 import method as method_cls
from .time_step_interval import time_step_interval as time_step_interval_cls
from .time_interval import time_interval as time_interval_cls
from .iteration_interval import iteration_interval as iteration_interval_cls
class solve_frequency(Group):
    """
    Enter radiation solve frequency.
    """

    fluent_name = "solve-frequency"

    child_names = \
        ['method', 'time_step_interval', 'time_interval',
         'iteration_interval']

    method: method_cls = method_cls
    """
    method child of solve_frequency.
    """
    time_step_interval: time_step_interval_cls = time_step_interval_cls
    """
    time_step_interval child of solve_frequency.
    """
    time_interval: time_interval_cls = time_interval_cls
    """
    time_interval child of solve_frequency.
    """
    iteration_interval: iteration_interval_cls = iteration_interval_cls
    """
    iteration_interval child of solve_frequency.
    """
