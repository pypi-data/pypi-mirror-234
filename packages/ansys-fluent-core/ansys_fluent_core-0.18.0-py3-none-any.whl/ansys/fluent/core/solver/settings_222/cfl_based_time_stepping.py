#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .courant_number_1 import courant_number as courant_number_cls
from .initial_time_step_size import initial_time_step_size as initial_time_step_size_cls
from .fixed_time_step_size import fixed_time_step_size as fixed_time_step_size_cls
from .min_time_step_size import min_time_step_size as min_time_step_size_cls
from .max_time_step_size import max_time_step_size as max_time_step_size_cls
from .min_step_change_factor import min_step_change_factor as min_step_change_factor_cls
from .max_step_change_factor import max_step_change_factor as max_step_change_factor_cls
from .update_interval import update_interval as update_interval_cls
class cfl_based_time_stepping(Group):
    """
    'cfl_based_time_stepping' child.
    """

    fluent_name = "cfl-based-time-stepping"

    child_names = \
        ['courant_number', 'initial_time_step_size', 'fixed_time_step_size',
         'min_time_step_size', 'max_time_step_size', 'min_step_change_factor',
         'max_step_change_factor', 'update_interval']

    courant_number: courant_number_cls = courant_number_cls
    """
    courant_number child of cfl_based_time_stepping.
    """
    initial_time_step_size: initial_time_step_size_cls = initial_time_step_size_cls
    """
    initial_time_step_size child of cfl_based_time_stepping.
    """
    fixed_time_step_size: fixed_time_step_size_cls = fixed_time_step_size_cls
    """
    fixed_time_step_size child of cfl_based_time_stepping.
    """
    min_time_step_size: min_time_step_size_cls = min_time_step_size_cls
    """
    min_time_step_size child of cfl_based_time_stepping.
    """
    max_time_step_size: max_time_step_size_cls = max_time_step_size_cls
    """
    max_time_step_size child of cfl_based_time_stepping.
    """
    min_step_change_factor: min_step_change_factor_cls = min_step_change_factor_cls
    """
    min_step_change_factor child of cfl_based_time_stepping.
    """
    max_step_change_factor: max_step_change_factor_cls = max_step_change_factor_cls
    """
    max_step_change_factor child of cfl_based_time_stepping.
    """
    update_interval: update_interval_cls = update_interval_cls
    """
    update_interval child of cfl_based_time_stepping.
    """
