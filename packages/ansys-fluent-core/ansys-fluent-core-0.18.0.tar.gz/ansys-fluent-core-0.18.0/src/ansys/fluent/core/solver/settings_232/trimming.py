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
from .thrust_coef import thrust_coef as thrust_coef_cls
from .pitch_moment_coef import pitch_moment_coef as pitch_moment_coef_cls
from .roll_moment_coef import roll_moment_coef as roll_moment_coef_cls
class trimming(Group):
    """
    Menu to define rotor trimming set-up.
    
     - trim-option       : to define collective and cyclic pitches to trim, 
     - update-frequency  : the number of solver iterations that pitch angle will be updated each time, 
     - damping-factor    : relaxation factor for pitch angles, 
     - thrust-coef       : desired thrust coefficient to set pitch for
     - pitch-moment-coef : desired pitch-moment coefficient to set pitch for, 
     - roll-moment-coef  : desired roll-moment coefficient to set pitch for, 
    
    For more details please consult the help option of the corresponding menu or TUI command.
    """

    fluent_name = "trimming"

    child_names = \
        ['trim_option', 'update_frequency', 'damping_factor', 'thrust_coef',
         'pitch_moment_coef', 'roll_moment_coef']

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
    thrust_coef: thrust_coef_cls = thrust_coef_cls
    """
    thrust_coef child of trimming.
    """
    pitch_moment_coef: pitch_moment_coef_cls = pitch_moment_coef_cls
    """
    pitch_moment_coef child of trimming.
    """
    roll_moment_coef: roll_moment_coef_cls = roll_moment_coef_cls
    """
    roll_moment_coef child of trimming.
    """
