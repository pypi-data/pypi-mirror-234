#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .min_pressure import min_pressure as min_pressure_cls
from .max_pressure import max_pressure as max_pressure_cls
from .min_temperature import min_temperature as min_temperature_cls
from .max_temperature import max_temperature as max_temperature_cls
from .min_tke import min_tke as min_tke_cls
from .min_lam_tke import min_lam_tke as min_lam_tke_cls
from .min_des_tke import min_des_tke as min_des_tke_cls
from .min_epsilon import min_epsilon as min_epsilon_cls
from .min_des_epsilon import min_des_epsilon as min_des_epsilon_cls
from .min_v2f_tke import min_v2f_tke as min_v2f_tke_cls
from .min_v2f_epsilon import min_v2f_epsilon as min_v2f_epsilon_cls
from .min_vel_var_scale import min_vel_var_scale as min_vel_var_scale_cls
from .min_elliptic_relax_func import min_elliptic_relax_func as min_elliptic_relax_func_cls
from .min_omega import min_omega as min_omega_cls
from .min_des_omega import min_des_omega as min_des_omega_cls
from .max_turb_visc_ratio import max_turb_visc_ratio as max_turb_visc_ratio_cls
from .positivity_rate import positivity_rate as positivity_rate_cls
from .min_vol_frac_for_matrix_sol import min_vol_frac_for_matrix_sol as min_vol_frac_for_matrix_sol_cls
class limits(Group):
    """
    'limits' child.
    """

    fluent_name = "limits"

    child_names = \
        ['min_pressure', 'max_pressure', 'min_temperature', 'max_temperature',
         'min_tke', 'min_lam_tke', 'min_des_tke', 'min_epsilon',
         'min_des_epsilon', 'min_v2f_tke', 'min_v2f_epsilon',
         'min_vel_var_scale', 'min_elliptic_relax_func', 'min_omega',
         'min_des_omega', 'max_turb_visc_ratio', 'positivity_rate',
         'min_vol_frac_for_matrix_sol']

    min_pressure: min_pressure_cls = min_pressure_cls
    """
    min_pressure child of limits.
    """
    max_pressure: max_pressure_cls = max_pressure_cls
    """
    max_pressure child of limits.
    """
    min_temperature: min_temperature_cls = min_temperature_cls
    """
    min_temperature child of limits.
    """
    max_temperature: max_temperature_cls = max_temperature_cls
    """
    max_temperature child of limits.
    """
    min_tke: min_tke_cls = min_tke_cls
    """
    min_tke child of limits.
    """
    min_lam_tke: min_lam_tke_cls = min_lam_tke_cls
    """
    min_lam_tke child of limits.
    """
    min_des_tke: min_des_tke_cls = min_des_tke_cls
    """
    min_des_tke child of limits.
    """
    min_epsilon: min_epsilon_cls = min_epsilon_cls
    """
    min_epsilon child of limits.
    """
    min_des_epsilon: min_des_epsilon_cls = min_des_epsilon_cls
    """
    min_des_epsilon child of limits.
    """
    min_v2f_tke: min_v2f_tke_cls = min_v2f_tke_cls
    """
    min_v2f_tke child of limits.
    """
    min_v2f_epsilon: min_v2f_epsilon_cls = min_v2f_epsilon_cls
    """
    min_v2f_epsilon child of limits.
    """
    min_vel_var_scale: min_vel_var_scale_cls = min_vel_var_scale_cls
    """
    min_vel_var_scale child of limits.
    """
    min_elliptic_relax_func: min_elliptic_relax_func_cls = min_elliptic_relax_func_cls
    """
    min_elliptic_relax_func child of limits.
    """
    min_omega: min_omega_cls = min_omega_cls
    """
    min_omega child of limits.
    """
    min_des_omega: min_des_omega_cls = min_des_omega_cls
    """
    min_des_omega child of limits.
    """
    max_turb_visc_ratio: max_turb_visc_ratio_cls = max_turb_visc_ratio_cls
    """
    max_turb_visc_ratio child of limits.
    """
    positivity_rate: positivity_rate_cls = positivity_rate_cls
    """
    positivity_rate child of limits.
    """
    min_vol_frac_for_matrix_sol: min_vol_frac_for_matrix_sol_cls = min_vol_frac_for_matrix_sol_cls
    """
    min_vol_frac_for_matrix_sol child of limits.
    """
