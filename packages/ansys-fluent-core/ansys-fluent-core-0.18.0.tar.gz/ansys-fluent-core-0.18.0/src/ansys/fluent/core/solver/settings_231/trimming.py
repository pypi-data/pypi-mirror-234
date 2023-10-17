#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .trim_option import trim_option as trim_option_cls
from .update_frequency import update_frequency as update_frequency_cls
from .damping_factor import damping_factor as damping_factor_cls
from .thrust_coefficient import thrust_coefficient as thrust_coefficient_cls
from .x_moment_coefficient import x_moment_coefficient as x_moment_coefficient_cls
from .y_moment_coefficient import y_moment_coefficient as y_moment_coefficient_cls
class trimming(Group):
    """
    Menu to define rotor trimming set-up.
    
     - trim-option       : to define collective and cyclic pitches to trim, 
     - update-frequency  : the number of solver iterations that pitch angle will be updated each time, 
     - damping-factor    : relaxation factor for pitch angles, 
     - thrust-coef       : desired thrust coefficient to set pitch for
     - moment-coef-x     : desired x-moment coefficient to set pitch for, 
     - moment-coef-y     : desired y-moment coefficient to set pitch for, 
    
    For more details please consult the help option of the corresponding menu or TUI command.
    """

    fluent_name = "trimming"

    child_names = \
        ['trim_option', 'update_frequency', 'damping_factor',
         'thrust_coefficient', 'x_moment_coefficient',
         'y_moment_coefficient']

    trim_option: trim_option_cls = trim_option_cls
    """
    trim_option child of trimming.
    """
    update_frequency: update_frequency_cls = update_frequency_cls
    """
    update_frequency child of trimming.
    """
    damping_factor: damping_factor_cls = damping_factor_cls
    """
    damping_factor child of trimming.
    """
    thrust_coefficient: thrust_coefficient_cls = thrust_coefficient_cls
    """
    thrust_coefficient child of trimming.
    """
    x_moment_coefficient: x_moment_coefficient_cls = x_moment_coefficient_cls
    """
    x_moment_coefficient child of trimming.
    """
    y_moment_coefficient: y_moment_coefficient_cls = y_moment_coefficient_cls
    """
    y_moment_coefficient child of trimming.
    """
