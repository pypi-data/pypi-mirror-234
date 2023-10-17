#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .pressure_max_lim import pressure_max_lim as pressure_max_lim_cls
from .pressure_min_lim import pressure_min_lim as pressure_min_lim_cls
from .temperature_max_lim import temperature_max_lim as temperature_max_lim_cls
from .temperature_min_lim import temperature_min_lim as temperature_min_lim_cls
from .k_min_lim import k_min_lim as k_min_lim_cls
from .k1_min_lim import k1_min_lim as k1_min_lim_cls
from .des_k_min_lim import des_k_min_lim as des_k_min_lim_cls
from .epsilon_min_lim import epsilon_min_lim as epsilon_min_lim_cls
from .des_epsilon_min_lim import des_epsilon_min_lim as des_epsilon_min_lim_cls
from .v2f_k_min_lim import v2f_k_min_lim as v2f_k_min_lim_cls
from .v2f_epsilon_min_lim import v2f_epsilon_min_lim as v2f_epsilon_min_lim_cls
from .v2f_v2_min_lim import v2f_v2_min_lim as v2f_v2_min_lim_cls
from .v2f_f_min_lim import v2f_f_min_lim as v2f_f_min_lim_cls
from .omega_min_lim import omega_min_lim as omega_min_lim_cls
from .des_omega_min_lim import des_omega_min_lim as des_omega_min_lim_cls
from .turb_visc_max_lim import turb_visc_max_lim as turb_visc_max_lim_cls
from .pos_lim import pos_lim as pos_lim_cls
from .matrix_solv_min_lim import matrix_solv_min_lim as matrix_solv_min_lim_cls
class limits(Group):
    """
    'limits' child.
    """

    fluent_name = "limits"

    child_names = \
        ['pressure_max_lim', 'pressure_min_lim', 'temperature_max_lim',
         'temperature_min_lim', 'k_min_lim', 'k1_min_lim', 'des_k_min_lim',
         'epsilon_min_lim', 'des_epsilon_min_lim', 'v2f_k_min_lim',
         'v2f_epsilon_min_lim', 'v2f_v2_min_lim', 'v2f_f_min_lim',
         'omega_min_lim', 'des_omega_min_lim', 'turb_visc_max_lim', 'pos_lim',
         'matrix_solv_min_lim']

    pressure_max_lim: pressure_max_lim_cls = pressure_max_lim_cls
    """
    pressure_max_lim child of limits.
    """
    pressure_min_lim: pressure_min_lim_cls = pressure_min_lim_cls
    """
    pressure_min_lim child of limits.
    """
    temperature_max_lim: temperature_max_lim_cls = temperature_max_lim_cls
    """
    temperature_max_lim child of limits.
    """
    temperature_min_lim: temperature_min_lim_cls = temperature_min_lim_cls
    """
    temperature_min_lim child of limits.
    """
    k_min_lim: k_min_lim_cls = k_min_lim_cls
    """
    k_min_lim child of limits.
    """
    k1_min_lim: k1_min_lim_cls = k1_min_lim_cls
    """
    k1_min_lim child of limits.
    """
    des_k_min_lim: des_k_min_lim_cls = des_k_min_lim_cls
    """
    des_k_min_lim child of limits.
    """
    epsilon_min_lim: epsilon_min_lim_cls = epsilon_min_lim_cls
    """
    epsilon_min_lim child of limits.
    """
    des_epsilon_min_lim: des_epsilon_min_lim_cls = des_epsilon_min_lim_cls
    """
    des_epsilon_min_lim child of limits.
    """
    v2f_k_min_lim: v2f_k_min_lim_cls = v2f_k_min_lim_cls
    """
    v2f_k_min_lim child of limits.
    """
    v2f_epsilon_min_lim: v2f_epsilon_min_lim_cls = v2f_epsilon_min_lim_cls
    """
    v2f_epsilon_min_lim child of limits.
    """
    v2f_v2_min_lim: v2f_v2_min_lim_cls = v2f_v2_min_lim_cls
    """
    v2f_v2_min_lim child of limits.
    """
    v2f_f_min_lim: v2f_f_min_lim_cls = v2f_f_min_lim_cls
    """
    v2f_f_min_lim child of limits.
    """
    omega_min_lim: omega_min_lim_cls = omega_min_lim_cls
    """
    omega_min_lim child of limits.
    """
    des_omega_min_lim: des_omega_min_lim_cls = des_omega_min_lim_cls
    """
    des_omega_min_lim child of limits.
    """
    turb_visc_max_lim: turb_visc_max_lim_cls = turb_visc_max_lim_cls
    """
    turb_visc_max_lim child of limits.
    """
    pos_lim: pos_lim_cls = pos_lim_cls
    """
    pos_lim child of limits.
    """
    matrix_solv_min_lim: matrix_solv_min_lim_cls = matrix_solv_min_lim_cls
    """
    matrix_solv_min_lim child of limits.
    """
