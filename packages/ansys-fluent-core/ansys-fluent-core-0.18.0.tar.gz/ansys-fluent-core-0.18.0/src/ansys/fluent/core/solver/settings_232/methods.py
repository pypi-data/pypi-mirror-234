#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .p_v_coupling import p_v_coupling as p_v_coupling_cls
from .flux_type_2 import flux_type as flux_type_cls
from .discretization_scheme import discretization_scheme as discretization_scheme_cls
from .pseudo_time_method import pseudo_time_method as pseudo_time_method_cls
from .unsteady_1st_order import unsteady_1st_order as unsteady_1st_order_cls
from .unsteady_2nd_order import unsteady_2nd_order as unsteady_2nd_order_cls
from .unsteady_2nd_order_bounded import unsteady_2nd_order_bounded as unsteady_2nd_order_bounded_cls
from .unsteady_global_time import unsteady_global_time as unsteady_global_time_cls
from .accelerated_non_iterative_time_marching import accelerated_non_iterative_time_marching as accelerated_non_iterative_time_marching_cls
from .convergence_acceleration_for_stretched_meshes_1 import convergence_acceleration_for_stretched_meshes as convergence_acceleration_for_stretched_meshes_cls
from .expert_1 import expert as expert_cls
from .frozen_flux import frozen_flux as frozen_flux_cls
from .gradient_scheme import gradient_scheme as gradient_scheme_cls
from .high_order_term_relaxation import high_order_term_relaxation as high_order_term_relaxation_cls
from .multiphase_numerics import multiphase_numerics as multiphase_numerics_cls
from .nb_gradient_boundary_option import nb_gradient_boundary_option as nb_gradient_boundary_option_cls
from .nita import nita as nita_cls
from .nita_expert_controls import nita_expert_controls as nita_expert_controls_cls
from .overset_1 import overset as overset_cls
from .phase_based_vof_discretization import phase_based_vof_discretization as phase_based_vof_discretization_cls
from .reduced_rank_extrapolation import reduced_rank_extrapolation as reduced_rank_extrapolation_cls
from .reduced_rank_extrapolation_options import reduced_rank_extrapolation_options as reduced_rank_extrapolation_options_cls
from .residual_smoothing import residual_smoothing as residual_smoothing_cls
from .vof_numerics import vof_numerics as vof_numerics_cls
from .warped_face_gradient_correction import warped_face_gradient_correction as warped_face_gradient_correction_cls
from .set_solution_methods_to_default import set_solution_methods_to_default as set_solution_methods_to_default_cls
class methods(Group):
    """
    'methods' child.
    """

    fluent_name = "methods"

    child_names = \
        ['p_v_coupling', 'flux_type', 'discretization_scheme',
         'pseudo_time_method', 'unsteady_1st_order', 'unsteady_2nd_order',
         'unsteady_2nd_order_bounded', 'unsteady_global_time',
         'accelerated_non_iterative_time_marching',
         'convergence_acceleration_for_stretched_meshes', 'expert',
         'frozen_flux', 'gradient_scheme', 'high_order_term_relaxation',
         'multiphase_numerics', 'nb_gradient_boundary_option', 'nita',
         'nita_expert_controls', 'overset', 'phase_based_vof_discretization',
         'reduced_rank_extrapolation', 'reduced_rank_extrapolation_options',
         'residual_smoothing', 'vof_numerics',
         'warped_face_gradient_correction']

    p_v_coupling: p_v_coupling_cls = p_v_coupling_cls
    """
    p_v_coupling child of methods.
    """
    flux_type: flux_type_cls = flux_type_cls
    """
    flux_type child of methods.
    """
    discretization_scheme: discretization_scheme_cls = discretization_scheme_cls
    """
    discretization_scheme child of methods.
    """
    pseudo_time_method: pseudo_time_method_cls = pseudo_time_method_cls
    """
    pseudo_time_method child of methods.
    """
    unsteady_1st_order: unsteady_1st_order_cls = unsteady_1st_order_cls
    """
    unsteady_1st_order child of methods.
    """
    unsteady_2nd_order: unsteady_2nd_order_cls = unsteady_2nd_order_cls
    """
    unsteady_2nd_order child of methods.
    """
    unsteady_2nd_order_bounded: unsteady_2nd_order_bounded_cls = unsteady_2nd_order_bounded_cls
    """
    unsteady_2nd_order_bounded child of methods.
    """
    unsteady_global_time: unsteady_global_time_cls = unsteady_global_time_cls
    """
    unsteady_global_time child of methods.
    """
    accelerated_non_iterative_time_marching: accelerated_non_iterative_time_marching_cls = accelerated_non_iterative_time_marching_cls
    """
    accelerated_non_iterative_time_marching child of methods.
    """
    convergence_acceleration_for_stretched_meshes: convergence_acceleration_for_stretched_meshes_cls = convergence_acceleration_for_stretched_meshes_cls
    """
    convergence_acceleration_for_stretched_meshes child of methods.
    """
    expert: expert_cls = expert_cls
    """
    expert child of methods.
    """
    frozen_flux: frozen_flux_cls = frozen_flux_cls
    """
    frozen_flux child of methods.
    """
    gradient_scheme: gradient_scheme_cls = gradient_scheme_cls
    """
    gradient_scheme child of methods.
    """
    high_order_term_relaxation: high_order_term_relaxation_cls = high_order_term_relaxation_cls
    """
    high_order_term_relaxation child of methods.
    """
    multiphase_numerics: multiphase_numerics_cls = multiphase_numerics_cls
    """
    multiphase_numerics child of methods.
    """
    nb_gradient_boundary_option: nb_gradient_boundary_option_cls = nb_gradient_boundary_option_cls
    """
    nb_gradient_boundary_option child of methods.
    """
    nita: nita_cls = nita_cls
    """
    nita child of methods.
    """
    nita_expert_controls: nita_expert_controls_cls = nita_expert_controls_cls
    """
    nita_expert_controls child of methods.
    """
    overset: overset_cls = overset_cls
    """
    overset child of methods.
    """
    phase_based_vof_discretization: phase_based_vof_discretization_cls = phase_based_vof_discretization_cls
    """
    phase_based_vof_discretization child of methods.
    """
    reduced_rank_extrapolation: reduced_rank_extrapolation_cls = reduced_rank_extrapolation_cls
    """
    reduced_rank_extrapolation child of methods.
    """
    reduced_rank_extrapolation_options: reduced_rank_extrapolation_options_cls = reduced_rank_extrapolation_options_cls
    """
    reduced_rank_extrapolation_options child of methods.
    """
    residual_smoothing: residual_smoothing_cls = residual_smoothing_cls
    """
    residual_smoothing child of methods.
    """
    vof_numerics: vof_numerics_cls = vof_numerics_cls
    """
    vof_numerics child of methods.
    """
    warped_face_gradient_correction: warped_face_gradient_correction_cls = warped_face_gradient_correction_cls
    """
    warped_face_gradient_correction child of methods.
    """
    command_names = \
        ['set_solution_methods_to_default']

    set_solution_methods_to_default: set_solution_methods_to_default_cls = set_solution_methods_to_default_cls
    """
    set_solution_methods_to_default command of methods.
    """
