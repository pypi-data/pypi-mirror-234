#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .courant_number import courant_number as courant_number_cls
from .p_v_controls import p_v_controls as p_v_controls_cls
from .relaxation_factor_1 import relaxation_factor as relaxation_factor_cls
from .under_relaxation_1 import under_relaxation as under_relaxation_cls
from .pseudo_time_method_local_time_step import pseudo_time_method_local_time_step as pseudo_time_method_local_time_step_cls
from .pseudo_time_explicit_relaxation_factor import pseudo_time_explicit_relaxation_factor as pseudo_time_explicit_relaxation_factor_cls
from .acoustics_wave_eqn_controls import acoustics_wave_eqn_controls as acoustics_wave_eqn_controls_cls
from .contact_solution_controls import contact_solution_controls as contact_solution_controls_cls
from .equations import equations as equations_cls
from .limits import limits as limits_cls
from .advanced import advanced as advanced_cls
from .reset_solution_controls import reset_solution_controls as reset_solution_controls_cls
from .reset_amg_controls import reset_amg_controls as reset_amg_controls_cls
from .reset_multi_stage_parameters import reset_multi_stage_parameters as reset_multi_stage_parameters_cls
from .reset_limits import reset_limits as reset_limits_cls
from .reset_pseudo_time_method_generic import reset_pseudo_time_method_generic as reset_pseudo_time_method_generic_cls
from .reset_pseudo_time_method_equations import reset_pseudo_time_method_equations as reset_pseudo_time_method_equations_cls
from .reset_pseudo_time_method_relaxations import reset_pseudo_time_method_relaxations as reset_pseudo_time_method_relaxations_cls
from .reset_pseudo_time_method_scale_factors import reset_pseudo_time_method_scale_factors as reset_pseudo_time_method_scale_factors_cls
class controls(Group):
    """
    'controls' child.
    """

    fluent_name = "controls"

    child_names = \
        ['courant_number', 'p_v_controls', 'relaxation_factor',
         'under_relaxation', 'pseudo_time_method_local_time_step',
         'pseudo_time_explicit_relaxation_factor',
         'acoustics_wave_eqn_controls', 'contact_solution_controls',
         'equations', 'limits', 'advanced']

    courant_number: courant_number_cls = courant_number_cls
    """
    courant_number child of controls.
    """
    p_v_controls: p_v_controls_cls = p_v_controls_cls
    """
    p_v_controls child of controls.
    """
    relaxation_factor: relaxation_factor_cls = relaxation_factor_cls
    """
    relaxation_factor child of controls.
    """
    under_relaxation: under_relaxation_cls = under_relaxation_cls
    """
    under_relaxation child of controls.
    """
    pseudo_time_method_local_time_step: pseudo_time_method_local_time_step_cls = pseudo_time_method_local_time_step_cls
    """
    pseudo_time_method_local_time_step child of controls.
    """
    pseudo_time_explicit_relaxation_factor: pseudo_time_explicit_relaxation_factor_cls = pseudo_time_explicit_relaxation_factor_cls
    """
    pseudo_time_explicit_relaxation_factor child of controls.
    """
    acoustics_wave_eqn_controls: acoustics_wave_eqn_controls_cls = acoustics_wave_eqn_controls_cls
    """
    acoustics_wave_eqn_controls child of controls.
    """
    contact_solution_controls: contact_solution_controls_cls = contact_solution_controls_cls
    """
    contact_solution_controls child of controls.
    """
    equations: equations_cls = equations_cls
    """
    equations child of controls.
    """
    limits: limits_cls = limits_cls
    """
    limits child of controls.
    """
    advanced: advanced_cls = advanced_cls
    """
    advanced child of controls.
    """
    command_names = \
        ['reset_solution_controls', 'reset_amg_controls',
         'reset_multi_stage_parameters', 'reset_limits',
         'reset_pseudo_time_method_generic',
         'reset_pseudo_time_method_equations',
         'reset_pseudo_time_method_relaxations',
         'reset_pseudo_time_method_scale_factors']

    reset_solution_controls: reset_solution_controls_cls = reset_solution_controls_cls
    """
    reset_solution_controls command of controls.
    """
    reset_amg_controls: reset_amg_controls_cls = reset_amg_controls_cls
    """
    reset_amg_controls command of controls.
    """
    reset_multi_stage_parameters: reset_multi_stage_parameters_cls = reset_multi_stage_parameters_cls
    """
    reset_multi_stage_parameters command of controls.
    """
    reset_limits: reset_limits_cls = reset_limits_cls
    """
    reset_limits command of controls.
    """
    reset_pseudo_time_method_generic: reset_pseudo_time_method_generic_cls = reset_pseudo_time_method_generic_cls
    """
    reset_pseudo_time_method_generic command of controls.
    """
    reset_pseudo_time_method_equations: reset_pseudo_time_method_equations_cls = reset_pseudo_time_method_equations_cls
    """
    reset_pseudo_time_method_equations command of controls.
    """
    reset_pseudo_time_method_relaxations: reset_pseudo_time_method_relaxations_cls = reset_pseudo_time_method_relaxations_cls
    """
    reset_pseudo_time_method_relaxations command of controls.
    """
    reset_pseudo_time_method_scale_factors: reset_pseudo_time_method_scale_factors_cls = reset_pseudo_time_method_scale_factors_cls
    """
    reset_pseudo_time_method_scale_factors command of controls.
    """
