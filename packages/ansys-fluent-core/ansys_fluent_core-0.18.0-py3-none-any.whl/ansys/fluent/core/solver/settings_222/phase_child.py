#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .material import material as material_cls
from .sources import sources as sources_cls
from .source_terms import source_terms as source_terms_cls
from .fixed import fixed as fixed_cls
from .cylindrical_fixed_var import cylindrical_fixed_var as cylindrical_fixed_var_cls
from .fixes import fixes as fixes_cls
from .motion_spec import motion_spec as motion_spec_cls
from .relative_to_thread import relative_to_thread as relative_to_thread_cls
from .omega import omega as omega_cls
from .axis_origin_component import axis_origin_component as axis_origin_component_cls
from .axis_direction_component import axis_direction_component as axis_direction_component_cls
from .udf_zmotion_name import udf_zmotion_name as udf_zmotion_name_cls
from .mrf_motion import mrf_motion as mrf_motion_cls
from .mrf_relative_to_thread import mrf_relative_to_thread as mrf_relative_to_thread_cls
from .mrf_omega import mrf_omega as mrf_omega_cls
from .reference_frame_velocity_components import reference_frame_velocity_components as reference_frame_velocity_components_cls
from .reference_frame_axis_origin_components import reference_frame_axis_origin_components as reference_frame_axis_origin_components_cls
from .reference_frame_axis_direction_components import reference_frame_axis_direction_components as reference_frame_axis_direction_components_cls
from .mrf_udf_zmotion_name import mrf_udf_zmotion_name as mrf_udf_zmotion_name_cls
from .mgrid_enable_transient import mgrid_enable_transient as mgrid_enable_transient_cls
from .mgrid_motion import mgrid_motion as mgrid_motion_cls
from .mgrid_relative_to_thread import mgrid_relative_to_thread as mgrid_relative_to_thread_cls
from .mgrid_omega import mgrid_omega as mgrid_omega_cls
from .moving_mesh_velocity_components import moving_mesh_velocity_components as moving_mesh_velocity_components_cls
from .moving_mesh_axis_origin_components import moving_mesh_axis_origin_components as moving_mesh_axis_origin_components_cls
from .mgrid_udf_zmotion_name import mgrid_udf_zmotion_name as mgrid_udf_zmotion_name_cls
from .solid_motion import solid_motion as solid_motion_cls
from .solid_relative_to_thread import solid_relative_to_thread as solid_relative_to_thread_cls
from .solid_omega import solid_omega as solid_omega_cls
from .solid_motion_velocity_components import solid_motion_velocity_components as solid_motion_velocity_components_cls
from .solid_motion_axis_origin_components import solid_motion_axis_origin_components as solid_motion_axis_origin_components_cls
from .solid_motion_axis_direction_components import solid_motion_axis_direction_components as solid_motion_axis_direction_components_cls
from .solid_udf_zmotion_name import solid_udf_zmotion_name as solid_udf_zmotion_name_cls
from .radiating import radiating as radiating_cls
from .les_embedded import les_embedded as les_embedded_cls
from .contact_property import contact_property as contact_property_cls
from .vapor_phase_realgas import vapor_phase_realgas as vapor_phase_realgas_cls
from .laminar import laminar as laminar_cls
from .laminar_mut_zero import laminar_mut_zero as laminar_mut_zero_cls
from .les_embedded_spec import les_embedded_spec as les_embedded_spec_cls
from .les_embedded_mom_scheme import les_embedded_mom_scheme as les_embedded_mom_scheme_cls
from .les_embedded_c_wale import les_embedded_c_wale as les_embedded_c_wale_cls
from .les_embedded_c_smag import les_embedded_c_smag as les_embedded_c_smag_cls
from .glass import glass as glass_cls
from .porous import porous as porous_cls
from .conical import conical as conical_cls
from .dir_spec_cond import dir_spec_cond as dir_spec_cond_cls
from .cursys import cursys as cursys_cls
from .cursys_name import cursys_name as cursys_name_cls
from .direction_1_x import direction_1_x as direction_1_x_cls
from .direction_1_y import direction_1_y as direction_1_y_cls
from .direction_1_z import direction_1_z as direction_1_z_cls
from .direction_2_x import direction_2_x as direction_2_x_cls
from .direction_2_y import direction_2_y as direction_2_y_cls
from .direction_2_z import direction_2_z as direction_2_z_cls
from .cone_axis_x import cone_axis_x as cone_axis_x_cls
from .cone_axis_y import cone_axis_y as cone_axis_y_cls
from .cone_axis_z import cone_axis_z as cone_axis_z_cls
from .cone_axis_pt_x import cone_axis_pt_x as cone_axis_pt_x_cls
from .cone_axis_pt_y import cone_axis_pt_y as cone_axis_pt_y_cls
from .cone_axis_pt_z import cone_axis_pt_z as cone_axis_pt_z_cls
from .cone_angle import cone_angle as cone_angle_cls
from .rel_vel_resistance import rel_vel_resistance as rel_vel_resistance_cls
from .porous_r_1 import porous_r_1 as porous_r_1_cls
from .porous_r_2 import porous_r_2 as porous_r_2_cls
from .porous_r_3 import porous_r_3 as porous_r_3_cls
from .alt_inertial_form import alt_inertial_form as alt_inertial_form_cls
from .porous_c_1 import porous_c_1 as porous_c_1_cls
from .porous_c_2 import porous_c_2 as porous_c_2_cls
from .porous_c_3 import porous_c_3 as porous_c_3_cls
from .c0 import c0 as c0_cls
from .c1 import c1 as c1_cls
from .porosity import porosity as porosity_cls
from .viscosity_ratio import viscosity_ratio as viscosity_ratio_cls
from .none import none as none_cls
from .corey import corey as corey_cls
from .stone_1 import stone_1 as stone_1_cls
from .stone_2 import stone_2 as stone_2_cls
from .rel_perm_limit_p1 import rel_perm_limit_p1 as rel_perm_limit_p1_cls
from .rel_perm_limit_p2 import rel_perm_limit_p2 as rel_perm_limit_p2_cls
from .ref_perm_p1 import ref_perm_p1 as ref_perm_p1_cls
from .exp_p1 import exp_p1 as exp_p1_cls
from .res_sat_p1 import res_sat_p1 as res_sat_p1_cls
from .ref_perm_p2 import ref_perm_p2 as ref_perm_p2_cls
from .exp_p2 import exp_p2 as exp_p2_cls
from .res_sat_p2 import res_sat_p2 as res_sat_p2_cls
from .ref_perm_p3 import ref_perm_p3 as ref_perm_p3_cls
from .exp_p3 import exp_p3 as exp_p3_cls
from .res_sat_p3 import res_sat_p3 as res_sat_p3_cls
from .capillary_pressure import capillary_pressure as capillary_pressure_cls
from .max_capillary_pressure import max_capillary_pressure as max_capillary_pressure_cls
from .van_genuchten_pg import van_genuchten_pg as van_genuchten_pg_cls
from .van_genuchten_ng import van_genuchten_ng as van_genuchten_ng_cls
from .skjaeveland_nw_pc_coef import skjaeveland_nw_pc_coef as skjaeveland_nw_pc_coef_cls
from .skjaeveland_nw_pc_pwr import skjaeveland_nw_pc_pwr as skjaeveland_nw_pc_pwr_cls
from .skjaeveland_wet_pc_coef import skjaeveland_wet_pc_coef as skjaeveland_wet_pc_coef_cls
from .skjaeveland_wet_pc_pwr import skjaeveland_wet_pc_pwr as skjaeveland_wet_pc_pwr_cls
from .brooks_corey_pe import brooks_corey_pe as brooks_corey_pe_cls
from .brooks_corey_ng import brooks_corey_ng as brooks_corey_ng_cls
from .leverett_con_ang import leverett_con_ang as leverett_con_ang_cls
from .rp_cbox_p1 import rp_cbox_p1 as rp_cbox_p1_cls
from .rp_edit_p1 import rp_edit_p1 as rp_edit_p1_cls
from .rel_perm_tabular_p1 import rel_perm_tabular_p1 as rel_perm_tabular_p1_cls
from .rel_perm_table_p1 import rel_perm_table_p1 as rel_perm_table_p1_cls
from .rel_perm_satw_p1 import rel_perm_satw_p1 as rel_perm_satw_p1_cls
from .rel_perm_rp_p1 import rel_perm_rp_p1 as rel_perm_rp_p1_cls
from .rp_cbox_p2 import rp_cbox_p2 as rp_cbox_p2_cls
from .rp_edit_p2 import rp_edit_p2 as rp_edit_p2_cls
from .rel_perm_tabular_p2 import rel_perm_tabular_p2 as rel_perm_tabular_p2_cls
from .rel_perm_table_p2 import rel_perm_table_p2 as rel_perm_table_p2_cls
from .rel_perm_satw_p2 import rel_perm_satw_p2 as rel_perm_satw_p2_cls
from .rel_perm_rp_p2 import rel_perm_rp_p2 as rel_perm_rp_p2_cls
from .wetting_phase import wetting_phase as wetting_phase_cls
from .non_wetting_phase import non_wetting_phase as non_wetting_phase_cls
from .equib_thermal import equib_thermal as equib_thermal_cls
from .non_equib_thermal import non_equib_thermal as non_equib_thermal_cls
from .solid_material import solid_material as solid_material_cls
from .area_density import area_density as area_density_cls
from .heat_transfer_coeff import heat_transfer_coeff as heat_transfer_coeff_cls
from .fanzone import fanzone as fanzone_cls
from .fan_zone_list import fan_zone_list as fan_zone_list_cls
from .fan_thickness import fan_thickness as fan_thickness_cls
from .fan_hub_rad import fan_hub_rad as fan_hub_rad_cls
from .fan_tip_rad import fan_tip_rad as fan_tip_rad_cls
from .fan_x_origin import fan_x_origin as fan_x_origin_cls
from .fan_y_origin import fan_y_origin as fan_y_origin_cls
from .fan_z_origin import fan_z_origin as fan_z_origin_cls
from .fan_rot_dir import fan_rot_dir as fan_rot_dir_cls
from .fan_opert_angvel import fan_opert_angvel as fan_opert_angvel_cls
from .fan_inflection_point import fan_inflection_point as fan_inflection_point_cls
from .limit_flow_fan import limit_flow_fan as limit_flow_fan_cls
from .max_flow_rate import max_flow_rate as max_flow_rate_cls
from .min_flow_rate import min_flow_rate as min_flow_rate_cls
from .tan_source_term import tan_source_term as tan_source_term_cls
from .rad_source_term import rad_source_term as rad_source_term_cls
from .axial_source_term import axial_source_term as axial_source_term_cls
from .fan_axial_source_method import fan_axial_source_method as fan_axial_source_method_cls
from .fan_pre_jump import fan_pre_jump as fan_pre_jump_cls
from .fan_curve_fit import fan_curve_fit as fan_curve_fit_cls
from .fan_poly_order import fan_poly_order as fan_poly_order_cls
from .fan_ini_flow import fan_ini_flow as fan_ini_flow_cls
from .fan_test_angvel import fan_test_angvel as fan_test_angvel_cls
from .fan_test_temp import fan_test_temp as fan_test_temp_cls
from .read_fan_curve import read_fan_curve as read_fan_curve_cls
from .reaction_mechs_1 import reaction_mechs as reaction_mechs_cls
from .react import react as react_cls
from .surface_volume_ratio import surface_volume_ratio as surface_volume_ratio_cls
from .electrolyte import electrolyte as electrolyte_cls
from .mp_compressive_beta_max import mp_compressive_beta_max as mp_compressive_beta_max_cls
from .mp_boiling_zone import mp_boiling_zone as mp_boiling_zone_cls
from .numerical_beach import numerical_beach as numerical_beach_cls
from .beach_id import beach_id as beach_id_cls
from .beach_multi_dir import beach_multi_dir as beach_multi_dir_cls
from .beach_damp_type import beach_damp_type as beach_damp_type_cls
from .beach_inlet_bndr import beach_inlet_bndr as beach_inlet_bndr_cls
from .beach_fs_level import beach_fs_level as beach_fs_level_cls
from .beach_bottom_level import beach_bottom_level as beach_bottom_level_cls
from .beach_dir_ni import beach_dir_ni as beach_dir_ni_cls
from .beach_dir_nj import beach_dir_nj as beach_dir_nj_cls
from .beach_dir_nk import beach_dir_nk as beach_dir_nk_cls
from .beach_damp_len_spec import beach_damp_len_spec as beach_damp_len_spec_cls
from .beach_wave_len import beach_wave_len as beach_wave_len_cls
from .beach_len_factor import beach_len_factor as beach_len_factor_cls
from .beach_start_point import beach_start_point as beach_start_point_cls
from .beach_end_point import beach_end_point as beach_end_point_cls
from .beach_dir_list import beach_dir_list as beach_dir_list_cls
from .beach_damp_relative import beach_damp_relative as beach_damp_relative_cls
from .beach_damp_resist_lin import beach_damp_resist_lin as beach_damp_resist_lin_cls
from .beach_damp_resist import beach_damp_resist as beach_damp_resist_cls
from .porous_structure import porous_structure as porous_structure_cls
from .structure_material import structure_material as structure_material_cls
from .anisotropic_spe_diff import anisotropic_spe_diff as anisotropic_spe_diff_cls
from .spe_diff_xx import spe_diff_xx as spe_diff_xx_cls
from .spe_diff_xy import spe_diff_xy as spe_diff_xy_cls
from .spe_diff_xz import spe_diff_xz as spe_diff_xz_cls
from .spe_diff_yx import spe_diff_yx as spe_diff_yx_cls
from .spe_diff_yy import spe_diff_yy as spe_diff_yy_cls
from .spe_diff_yz import spe_diff_yz as spe_diff_yz_cls
from .spe_diff_zx import spe_diff_zx as spe_diff_zx_cls
from .spe_diff_zy import spe_diff_zy as spe_diff_zy_cls
from .spe_diff_zz import spe_diff_zz as spe_diff_zz_cls
class phase_child(Group):
    """
    'child_object_type' of phase.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['material', 'sources', 'source_terms', 'fixed',
         'cylindrical_fixed_var', 'fixes', 'motion_spec',
         'relative_to_thread', 'omega', 'axis_origin_component',
         'axis_direction_component', 'udf_zmotion_name', 'mrf_motion',
         'mrf_relative_to_thread', 'mrf_omega',
         'reference_frame_velocity_components',
         'reference_frame_axis_origin_components',
         'reference_frame_axis_direction_components', 'mrf_udf_zmotion_name',
         'mgrid_enable_transient', 'mgrid_motion', 'mgrid_relative_to_thread',
         'mgrid_omega', 'moving_mesh_velocity_components',
         'moving_mesh_axis_origin_components', 'mgrid_udf_zmotion_name',
         'solid_motion', 'solid_relative_to_thread', 'solid_omega',
         'solid_motion_velocity_components',
         'solid_motion_axis_origin_components',
         'solid_motion_axis_direction_components', 'solid_udf_zmotion_name',
         'radiating', 'les_embedded', 'contact_property',
         'vapor_phase_realgas', 'laminar', 'laminar_mut_zero',
         'les_embedded_spec', 'les_embedded_mom_scheme',
         'les_embedded_c_wale', 'les_embedded_c_smag', 'glass', 'porous',
         'conical', 'dir_spec_cond', 'cursys', 'cursys_name', 'direction_1_x',
         'direction_1_y', 'direction_1_z', 'direction_2_x', 'direction_2_y',
         'direction_2_z', 'cone_axis_x', 'cone_axis_y', 'cone_axis_z',
         'cone_axis_pt_x', 'cone_axis_pt_y', 'cone_axis_pt_z', 'cone_angle',
         'rel_vel_resistance', 'porous_r_1', 'porous_r_2', 'porous_r_3',
         'alt_inertial_form', 'porous_c_1', 'porous_c_2', 'porous_c_3', 'c0',
         'c1', 'porosity', 'viscosity_ratio', 'none', 'corey', 'stone_1',
         'stone_2', 'rel_perm_limit_p1', 'rel_perm_limit_p2', 'ref_perm_p1',
         'exp_p1', 'res_sat_p1', 'ref_perm_p2', 'exp_p2', 'res_sat_p2',
         'ref_perm_p3', 'exp_p3', 'res_sat_p3', 'capillary_pressure',
         'max_capillary_pressure', 'van_genuchten_pg', 'van_genuchten_ng',
         'skjaeveland_nw_pc_coef', 'skjaeveland_nw_pc_pwr',
         'skjaeveland_wet_pc_coef', 'skjaeveland_wet_pc_pwr',
         'brooks_corey_pe', 'brooks_corey_ng', 'leverett_con_ang',
         'rp_cbox_p1', 'rp_edit_p1', 'rel_perm_tabular_p1',
         'rel_perm_table_p1', 'rel_perm_satw_p1', 'rel_perm_rp_p1',
         'rp_cbox_p2', 'rp_edit_p2', 'rel_perm_tabular_p2',
         'rel_perm_table_p2', 'rel_perm_satw_p2', 'rel_perm_rp_p2',
         'wetting_phase', 'non_wetting_phase', 'equib_thermal',
         'non_equib_thermal', 'solid_material', 'area_density',
         'heat_transfer_coeff', 'fanzone', 'fan_zone_list', 'fan_thickness',
         'fan_hub_rad', 'fan_tip_rad', 'fan_x_origin', 'fan_y_origin',
         'fan_z_origin', 'fan_rot_dir', 'fan_opert_angvel',
         'fan_inflection_point', 'limit_flow_fan', 'max_flow_rate',
         'min_flow_rate', 'tan_source_term', 'rad_source_term',
         'axial_source_term', 'fan_axial_source_method', 'fan_pre_jump',
         'fan_curve_fit', 'fan_poly_order', 'fan_ini_flow', 'fan_test_angvel',
         'fan_test_temp', 'read_fan_curve', 'reaction_mechs', 'react',
         'surface_volume_ratio', 'electrolyte', 'mp_compressive_beta_max',
         'mp_boiling_zone', 'numerical_beach', 'beach_id', 'beach_multi_dir',
         'beach_damp_type', 'beach_inlet_bndr', 'beach_fs_level',
         'beach_bottom_level', 'beach_dir_ni', 'beach_dir_nj', 'beach_dir_nk',
         'beach_damp_len_spec', 'beach_wave_len', 'beach_len_factor',
         'beach_start_point', 'beach_end_point', 'beach_dir_list',
         'beach_damp_relative', 'beach_damp_resist_lin', 'beach_damp_resist',
         'porous_structure', 'structure_material', 'anisotropic_spe_diff',
         'spe_diff_xx', 'spe_diff_xy', 'spe_diff_xz', 'spe_diff_yx',
         'spe_diff_yy', 'spe_diff_yz', 'spe_diff_zx', 'spe_diff_zy',
         'spe_diff_zz']

    material: material_cls = material_cls
    """
    material child of phase_child.
    """
    sources: sources_cls = sources_cls
    """
    sources child of phase_child.
    """
    source_terms: source_terms_cls = source_terms_cls
    """
    source_terms child of phase_child.
    """
    fixed: fixed_cls = fixed_cls
    """
    fixed child of phase_child.
    """
    cylindrical_fixed_var: cylindrical_fixed_var_cls = cylindrical_fixed_var_cls
    """
    cylindrical_fixed_var child of phase_child.
    """
    fixes: fixes_cls = fixes_cls
    """
    fixes child of phase_child.
    """
    motion_spec: motion_spec_cls = motion_spec_cls
    """
    motion_spec child of phase_child.
    """
    relative_to_thread: relative_to_thread_cls = relative_to_thread_cls
    """
    relative_to_thread child of phase_child.
    """
    omega: omega_cls = omega_cls
    """
    omega child of phase_child.
    """
    axis_origin_component: axis_origin_component_cls = axis_origin_component_cls
    """
    axis_origin_component child of phase_child.
    """
    axis_direction_component: axis_direction_component_cls = axis_direction_component_cls
    """
    axis_direction_component child of phase_child.
    """
    udf_zmotion_name: udf_zmotion_name_cls = udf_zmotion_name_cls
    """
    udf_zmotion_name child of phase_child.
    """
    mrf_motion: mrf_motion_cls = mrf_motion_cls
    """
    mrf_motion child of phase_child.
    """
    mrf_relative_to_thread: mrf_relative_to_thread_cls = mrf_relative_to_thread_cls
    """
    mrf_relative_to_thread child of phase_child.
    """
    mrf_omega: mrf_omega_cls = mrf_omega_cls
    """
    mrf_omega child of phase_child.
    """
    reference_frame_velocity_components: reference_frame_velocity_components_cls = reference_frame_velocity_components_cls
    """
    reference_frame_velocity_components child of phase_child.
    """
    reference_frame_axis_origin_components: reference_frame_axis_origin_components_cls = reference_frame_axis_origin_components_cls
    """
    reference_frame_axis_origin_components child of phase_child.
    """
    reference_frame_axis_direction_components: reference_frame_axis_direction_components_cls = reference_frame_axis_direction_components_cls
    """
    reference_frame_axis_direction_components child of phase_child.
    """
    mrf_udf_zmotion_name: mrf_udf_zmotion_name_cls = mrf_udf_zmotion_name_cls
    """
    mrf_udf_zmotion_name child of phase_child.
    """
    mgrid_enable_transient: mgrid_enable_transient_cls = mgrid_enable_transient_cls
    """
    mgrid_enable_transient child of phase_child.
    """
    mgrid_motion: mgrid_motion_cls = mgrid_motion_cls
    """
    mgrid_motion child of phase_child.
    """
    mgrid_relative_to_thread: mgrid_relative_to_thread_cls = mgrid_relative_to_thread_cls
    """
    mgrid_relative_to_thread child of phase_child.
    """
    mgrid_omega: mgrid_omega_cls = mgrid_omega_cls
    """
    mgrid_omega child of phase_child.
    """
    moving_mesh_velocity_components: moving_mesh_velocity_components_cls = moving_mesh_velocity_components_cls
    """
    moving_mesh_velocity_components child of phase_child.
    """
    moving_mesh_axis_origin_components: moving_mesh_axis_origin_components_cls = moving_mesh_axis_origin_components_cls
    """
    moving_mesh_axis_origin_components child of phase_child.
    """
    mgrid_udf_zmotion_name: mgrid_udf_zmotion_name_cls = mgrid_udf_zmotion_name_cls
    """
    mgrid_udf_zmotion_name child of phase_child.
    """
    solid_motion: solid_motion_cls = solid_motion_cls
    """
    solid_motion child of phase_child.
    """
    solid_relative_to_thread: solid_relative_to_thread_cls = solid_relative_to_thread_cls
    """
    solid_relative_to_thread child of phase_child.
    """
    solid_omega: solid_omega_cls = solid_omega_cls
    """
    solid_omega child of phase_child.
    """
    solid_motion_velocity_components: solid_motion_velocity_components_cls = solid_motion_velocity_components_cls
    """
    solid_motion_velocity_components child of phase_child.
    """
    solid_motion_axis_origin_components: solid_motion_axis_origin_components_cls = solid_motion_axis_origin_components_cls
    """
    solid_motion_axis_origin_components child of phase_child.
    """
    solid_motion_axis_direction_components: solid_motion_axis_direction_components_cls = solid_motion_axis_direction_components_cls
    """
    solid_motion_axis_direction_components child of phase_child.
    """
    solid_udf_zmotion_name: solid_udf_zmotion_name_cls = solid_udf_zmotion_name_cls
    """
    solid_udf_zmotion_name child of phase_child.
    """
    radiating: radiating_cls = radiating_cls
    """
    radiating child of phase_child.
    """
    les_embedded: les_embedded_cls = les_embedded_cls
    """
    les_embedded child of phase_child.
    """
    contact_property: contact_property_cls = contact_property_cls
    """
    contact_property child of phase_child.
    """
    vapor_phase_realgas: vapor_phase_realgas_cls = vapor_phase_realgas_cls
    """
    vapor_phase_realgas child of phase_child.
    """
    laminar: laminar_cls = laminar_cls
    """
    laminar child of phase_child.
    """
    laminar_mut_zero: laminar_mut_zero_cls = laminar_mut_zero_cls
    """
    laminar_mut_zero child of phase_child.
    """
    les_embedded_spec: les_embedded_spec_cls = les_embedded_spec_cls
    """
    les_embedded_spec child of phase_child.
    """
    les_embedded_mom_scheme: les_embedded_mom_scheme_cls = les_embedded_mom_scheme_cls
    """
    les_embedded_mom_scheme child of phase_child.
    """
    les_embedded_c_wale: les_embedded_c_wale_cls = les_embedded_c_wale_cls
    """
    les_embedded_c_wale child of phase_child.
    """
    les_embedded_c_smag: les_embedded_c_smag_cls = les_embedded_c_smag_cls
    """
    les_embedded_c_smag child of phase_child.
    """
    glass: glass_cls = glass_cls
    """
    glass child of phase_child.
    """
    porous: porous_cls = porous_cls
    """
    porous child of phase_child.
    """
    conical: conical_cls = conical_cls
    """
    conical child of phase_child.
    """
    dir_spec_cond: dir_spec_cond_cls = dir_spec_cond_cls
    """
    dir_spec_cond child of phase_child.
    """
    cursys: cursys_cls = cursys_cls
    """
    cursys child of phase_child.
    """
    cursys_name: cursys_name_cls = cursys_name_cls
    """
    cursys_name child of phase_child.
    """
    direction_1_x: direction_1_x_cls = direction_1_x_cls
    """
    direction_1_x child of phase_child.
    """
    direction_1_y: direction_1_y_cls = direction_1_y_cls
    """
    direction_1_y child of phase_child.
    """
    direction_1_z: direction_1_z_cls = direction_1_z_cls
    """
    direction_1_z child of phase_child.
    """
    direction_2_x: direction_2_x_cls = direction_2_x_cls
    """
    direction_2_x child of phase_child.
    """
    direction_2_y: direction_2_y_cls = direction_2_y_cls
    """
    direction_2_y child of phase_child.
    """
    direction_2_z: direction_2_z_cls = direction_2_z_cls
    """
    direction_2_z child of phase_child.
    """
    cone_axis_x: cone_axis_x_cls = cone_axis_x_cls
    """
    cone_axis_x child of phase_child.
    """
    cone_axis_y: cone_axis_y_cls = cone_axis_y_cls
    """
    cone_axis_y child of phase_child.
    """
    cone_axis_z: cone_axis_z_cls = cone_axis_z_cls
    """
    cone_axis_z child of phase_child.
    """
    cone_axis_pt_x: cone_axis_pt_x_cls = cone_axis_pt_x_cls
    """
    cone_axis_pt_x child of phase_child.
    """
    cone_axis_pt_y: cone_axis_pt_y_cls = cone_axis_pt_y_cls
    """
    cone_axis_pt_y child of phase_child.
    """
    cone_axis_pt_z: cone_axis_pt_z_cls = cone_axis_pt_z_cls
    """
    cone_axis_pt_z child of phase_child.
    """
    cone_angle: cone_angle_cls = cone_angle_cls
    """
    cone_angle child of phase_child.
    """
    rel_vel_resistance: rel_vel_resistance_cls = rel_vel_resistance_cls
    """
    rel_vel_resistance child of phase_child.
    """
    porous_r_1: porous_r_1_cls = porous_r_1_cls
    """
    porous_r_1 child of phase_child.
    """
    porous_r_2: porous_r_2_cls = porous_r_2_cls
    """
    porous_r_2 child of phase_child.
    """
    porous_r_3: porous_r_3_cls = porous_r_3_cls
    """
    porous_r_3 child of phase_child.
    """
    alt_inertial_form: alt_inertial_form_cls = alt_inertial_form_cls
    """
    alt_inertial_form child of phase_child.
    """
    porous_c_1: porous_c_1_cls = porous_c_1_cls
    """
    porous_c_1 child of phase_child.
    """
    porous_c_2: porous_c_2_cls = porous_c_2_cls
    """
    porous_c_2 child of phase_child.
    """
    porous_c_3: porous_c_3_cls = porous_c_3_cls
    """
    porous_c_3 child of phase_child.
    """
    c0: c0_cls = c0_cls
    """
    c0 child of phase_child.
    """
    c1: c1_cls = c1_cls
    """
    c1 child of phase_child.
    """
    porosity: porosity_cls = porosity_cls
    """
    porosity child of phase_child.
    """
    viscosity_ratio: viscosity_ratio_cls = viscosity_ratio_cls
    """
    viscosity_ratio child of phase_child.
    """
    none: none_cls = none_cls
    """
    none child of phase_child.
    """
    corey: corey_cls = corey_cls
    """
    corey child of phase_child.
    """
    stone_1: stone_1_cls = stone_1_cls
    """
    stone_1 child of phase_child.
    """
    stone_2: stone_2_cls = stone_2_cls
    """
    stone_2 child of phase_child.
    """
    rel_perm_limit_p1: rel_perm_limit_p1_cls = rel_perm_limit_p1_cls
    """
    rel_perm_limit_p1 child of phase_child.
    """
    rel_perm_limit_p2: rel_perm_limit_p2_cls = rel_perm_limit_p2_cls
    """
    rel_perm_limit_p2 child of phase_child.
    """
    ref_perm_p1: ref_perm_p1_cls = ref_perm_p1_cls
    """
    ref_perm_p1 child of phase_child.
    """
    exp_p1: exp_p1_cls = exp_p1_cls
    """
    exp_p1 child of phase_child.
    """
    res_sat_p1: res_sat_p1_cls = res_sat_p1_cls
    """
    res_sat_p1 child of phase_child.
    """
    ref_perm_p2: ref_perm_p2_cls = ref_perm_p2_cls
    """
    ref_perm_p2 child of phase_child.
    """
    exp_p2: exp_p2_cls = exp_p2_cls
    """
    exp_p2 child of phase_child.
    """
    res_sat_p2: res_sat_p2_cls = res_sat_p2_cls
    """
    res_sat_p2 child of phase_child.
    """
    ref_perm_p3: ref_perm_p3_cls = ref_perm_p3_cls
    """
    ref_perm_p3 child of phase_child.
    """
    exp_p3: exp_p3_cls = exp_p3_cls
    """
    exp_p3 child of phase_child.
    """
    res_sat_p3: res_sat_p3_cls = res_sat_p3_cls
    """
    res_sat_p3 child of phase_child.
    """
    capillary_pressure: capillary_pressure_cls = capillary_pressure_cls
    """
    capillary_pressure child of phase_child.
    """
    max_capillary_pressure: max_capillary_pressure_cls = max_capillary_pressure_cls
    """
    max_capillary_pressure child of phase_child.
    """
    van_genuchten_pg: van_genuchten_pg_cls = van_genuchten_pg_cls
    """
    van_genuchten_pg child of phase_child.
    """
    van_genuchten_ng: van_genuchten_ng_cls = van_genuchten_ng_cls
    """
    van_genuchten_ng child of phase_child.
    """
    skjaeveland_nw_pc_coef: skjaeveland_nw_pc_coef_cls = skjaeveland_nw_pc_coef_cls
    """
    skjaeveland_nw_pc_coef child of phase_child.
    """
    skjaeveland_nw_pc_pwr: skjaeveland_nw_pc_pwr_cls = skjaeveland_nw_pc_pwr_cls
    """
    skjaeveland_nw_pc_pwr child of phase_child.
    """
    skjaeveland_wet_pc_coef: skjaeveland_wet_pc_coef_cls = skjaeveland_wet_pc_coef_cls
    """
    skjaeveland_wet_pc_coef child of phase_child.
    """
    skjaeveland_wet_pc_pwr: skjaeveland_wet_pc_pwr_cls = skjaeveland_wet_pc_pwr_cls
    """
    skjaeveland_wet_pc_pwr child of phase_child.
    """
    brooks_corey_pe: brooks_corey_pe_cls = brooks_corey_pe_cls
    """
    brooks_corey_pe child of phase_child.
    """
    brooks_corey_ng: brooks_corey_ng_cls = brooks_corey_ng_cls
    """
    brooks_corey_ng child of phase_child.
    """
    leverett_con_ang: leverett_con_ang_cls = leverett_con_ang_cls
    """
    leverett_con_ang child of phase_child.
    """
    rp_cbox_p1: rp_cbox_p1_cls = rp_cbox_p1_cls
    """
    rp_cbox_p1 child of phase_child.
    """
    rp_edit_p1: rp_edit_p1_cls = rp_edit_p1_cls
    """
    rp_edit_p1 child of phase_child.
    """
    rel_perm_tabular_p1: rel_perm_tabular_p1_cls = rel_perm_tabular_p1_cls
    """
    rel_perm_tabular_p1 child of phase_child.
    """
    rel_perm_table_p1: rel_perm_table_p1_cls = rel_perm_table_p1_cls
    """
    rel_perm_table_p1 child of phase_child.
    """
    rel_perm_satw_p1: rel_perm_satw_p1_cls = rel_perm_satw_p1_cls
    """
    rel_perm_satw_p1 child of phase_child.
    """
    rel_perm_rp_p1: rel_perm_rp_p1_cls = rel_perm_rp_p1_cls
    """
    rel_perm_rp_p1 child of phase_child.
    """
    rp_cbox_p2: rp_cbox_p2_cls = rp_cbox_p2_cls
    """
    rp_cbox_p2 child of phase_child.
    """
    rp_edit_p2: rp_edit_p2_cls = rp_edit_p2_cls
    """
    rp_edit_p2 child of phase_child.
    """
    rel_perm_tabular_p2: rel_perm_tabular_p2_cls = rel_perm_tabular_p2_cls
    """
    rel_perm_tabular_p2 child of phase_child.
    """
    rel_perm_table_p2: rel_perm_table_p2_cls = rel_perm_table_p2_cls
    """
    rel_perm_table_p2 child of phase_child.
    """
    rel_perm_satw_p2: rel_perm_satw_p2_cls = rel_perm_satw_p2_cls
    """
    rel_perm_satw_p2 child of phase_child.
    """
    rel_perm_rp_p2: rel_perm_rp_p2_cls = rel_perm_rp_p2_cls
    """
    rel_perm_rp_p2 child of phase_child.
    """
    wetting_phase: wetting_phase_cls = wetting_phase_cls
    """
    wetting_phase child of phase_child.
    """
    non_wetting_phase: non_wetting_phase_cls = non_wetting_phase_cls
    """
    non_wetting_phase child of phase_child.
    """
    equib_thermal: equib_thermal_cls = equib_thermal_cls
    """
    equib_thermal child of phase_child.
    """
    non_equib_thermal: non_equib_thermal_cls = non_equib_thermal_cls
    """
    non_equib_thermal child of phase_child.
    """
    solid_material: solid_material_cls = solid_material_cls
    """
    solid_material child of phase_child.
    """
    area_density: area_density_cls = area_density_cls
    """
    area_density child of phase_child.
    """
    heat_transfer_coeff: heat_transfer_coeff_cls = heat_transfer_coeff_cls
    """
    heat_transfer_coeff child of phase_child.
    """
    fanzone: fanzone_cls = fanzone_cls
    """
    fanzone child of phase_child.
    """
    fan_zone_list: fan_zone_list_cls = fan_zone_list_cls
    """
    fan_zone_list child of phase_child.
    """
    fan_thickness: fan_thickness_cls = fan_thickness_cls
    """
    fan_thickness child of phase_child.
    """
    fan_hub_rad: fan_hub_rad_cls = fan_hub_rad_cls
    """
    fan_hub_rad child of phase_child.
    """
    fan_tip_rad: fan_tip_rad_cls = fan_tip_rad_cls
    """
    fan_tip_rad child of phase_child.
    """
    fan_x_origin: fan_x_origin_cls = fan_x_origin_cls
    """
    fan_x_origin child of phase_child.
    """
    fan_y_origin: fan_y_origin_cls = fan_y_origin_cls
    """
    fan_y_origin child of phase_child.
    """
    fan_z_origin: fan_z_origin_cls = fan_z_origin_cls
    """
    fan_z_origin child of phase_child.
    """
    fan_rot_dir: fan_rot_dir_cls = fan_rot_dir_cls
    """
    fan_rot_dir child of phase_child.
    """
    fan_opert_angvel: fan_opert_angvel_cls = fan_opert_angvel_cls
    """
    fan_opert_angvel child of phase_child.
    """
    fan_inflection_point: fan_inflection_point_cls = fan_inflection_point_cls
    """
    fan_inflection_point child of phase_child.
    """
    limit_flow_fan: limit_flow_fan_cls = limit_flow_fan_cls
    """
    limit_flow_fan child of phase_child.
    """
    max_flow_rate: max_flow_rate_cls = max_flow_rate_cls
    """
    max_flow_rate child of phase_child.
    """
    min_flow_rate: min_flow_rate_cls = min_flow_rate_cls
    """
    min_flow_rate child of phase_child.
    """
    tan_source_term: tan_source_term_cls = tan_source_term_cls
    """
    tan_source_term child of phase_child.
    """
    rad_source_term: rad_source_term_cls = rad_source_term_cls
    """
    rad_source_term child of phase_child.
    """
    axial_source_term: axial_source_term_cls = axial_source_term_cls
    """
    axial_source_term child of phase_child.
    """
    fan_axial_source_method: fan_axial_source_method_cls = fan_axial_source_method_cls
    """
    fan_axial_source_method child of phase_child.
    """
    fan_pre_jump: fan_pre_jump_cls = fan_pre_jump_cls
    """
    fan_pre_jump child of phase_child.
    """
    fan_curve_fit: fan_curve_fit_cls = fan_curve_fit_cls
    """
    fan_curve_fit child of phase_child.
    """
    fan_poly_order: fan_poly_order_cls = fan_poly_order_cls
    """
    fan_poly_order child of phase_child.
    """
    fan_ini_flow: fan_ini_flow_cls = fan_ini_flow_cls
    """
    fan_ini_flow child of phase_child.
    """
    fan_test_angvel: fan_test_angvel_cls = fan_test_angvel_cls
    """
    fan_test_angvel child of phase_child.
    """
    fan_test_temp: fan_test_temp_cls = fan_test_temp_cls
    """
    fan_test_temp child of phase_child.
    """
    read_fan_curve: read_fan_curve_cls = read_fan_curve_cls
    """
    read_fan_curve child of phase_child.
    """
    reaction_mechs: reaction_mechs_cls = reaction_mechs_cls
    """
    reaction_mechs child of phase_child.
    """
    react: react_cls = react_cls
    """
    react child of phase_child.
    """
    surface_volume_ratio: surface_volume_ratio_cls = surface_volume_ratio_cls
    """
    surface_volume_ratio child of phase_child.
    """
    electrolyte: electrolyte_cls = electrolyte_cls
    """
    electrolyte child of phase_child.
    """
    mp_compressive_beta_max: mp_compressive_beta_max_cls = mp_compressive_beta_max_cls
    """
    mp_compressive_beta_max child of phase_child.
    """
    mp_boiling_zone: mp_boiling_zone_cls = mp_boiling_zone_cls
    """
    mp_boiling_zone child of phase_child.
    """
    numerical_beach: numerical_beach_cls = numerical_beach_cls
    """
    numerical_beach child of phase_child.
    """
    beach_id: beach_id_cls = beach_id_cls
    """
    beach_id child of phase_child.
    """
    beach_multi_dir: beach_multi_dir_cls = beach_multi_dir_cls
    """
    beach_multi_dir child of phase_child.
    """
    beach_damp_type: beach_damp_type_cls = beach_damp_type_cls
    """
    beach_damp_type child of phase_child.
    """
    beach_inlet_bndr: beach_inlet_bndr_cls = beach_inlet_bndr_cls
    """
    beach_inlet_bndr child of phase_child.
    """
    beach_fs_level: beach_fs_level_cls = beach_fs_level_cls
    """
    beach_fs_level child of phase_child.
    """
    beach_bottom_level: beach_bottom_level_cls = beach_bottom_level_cls
    """
    beach_bottom_level child of phase_child.
    """
    beach_dir_ni: beach_dir_ni_cls = beach_dir_ni_cls
    """
    beach_dir_ni child of phase_child.
    """
    beach_dir_nj: beach_dir_nj_cls = beach_dir_nj_cls
    """
    beach_dir_nj child of phase_child.
    """
    beach_dir_nk: beach_dir_nk_cls = beach_dir_nk_cls
    """
    beach_dir_nk child of phase_child.
    """
    beach_damp_len_spec: beach_damp_len_spec_cls = beach_damp_len_spec_cls
    """
    beach_damp_len_spec child of phase_child.
    """
    beach_wave_len: beach_wave_len_cls = beach_wave_len_cls
    """
    beach_wave_len child of phase_child.
    """
    beach_len_factor: beach_len_factor_cls = beach_len_factor_cls
    """
    beach_len_factor child of phase_child.
    """
    beach_start_point: beach_start_point_cls = beach_start_point_cls
    """
    beach_start_point child of phase_child.
    """
    beach_end_point: beach_end_point_cls = beach_end_point_cls
    """
    beach_end_point child of phase_child.
    """
    beach_dir_list: beach_dir_list_cls = beach_dir_list_cls
    """
    beach_dir_list child of phase_child.
    """
    beach_damp_relative: beach_damp_relative_cls = beach_damp_relative_cls
    """
    beach_damp_relative child of phase_child.
    """
    beach_damp_resist_lin: beach_damp_resist_lin_cls = beach_damp_resist_lin_cls
    """
    beach_damp_resist_lin child of phase_child.
    """
    beach_damp_resist: beach_damp_resist_cls = beach_damp_resist_cls
    """
    beach_damp_resist child of phase_child.
    """
    porous_structure: porous_structure_cls = porous_structure_cls
    """
    porous_structure child of phase_child.
    """
    structure_material: structure_material_cls = structure_material_cls
    """
    structure_material child of phase_child.
    """
    anisotropic_spe_diff: anisotropic_spe_diff_cls = anisotropic_spe_diff_cls
    """
    anisotropic_spe_diff child of phase_child.
    """
    spe_diff_xx: spe_diff_xx_cls = spe_diff_xx_cls
    """
    spe_diff_xx child of phase_child.
    """
    spe_diff_xy: spe_diff_xy_cls = spe_diff_xy_cls
    """
    spe_diff_xy child of phase_child.
    """
    spe_diff_xz: spe_diff_xz_cls = spe_diff_xz_cls
    """
    spe_diff_xz child of phase_child.
    """
    spe_diff_yx: spe_diff_yx_cls = spe_diff_yx_cls
    """
    spe_diff_yx child of phase_child.
    """
    spe_diff_yy: spe_diff_yy_cls = spe_diff_yy_cls
    """
    spe_diff_yy child of phase_child.
    """
    spe_diff_yz: spe_diff_yz_cls = spe_diff_yz_cls
    """
    spe_diff_yz child of phase_child.
    """
    spe_diff_zx: spe_diff_zx_cls = spe_diff_zx_cls
    """
    spe_diff_zx child of phase_child.
    """
    spe_diff_zy: spe_diff_zy_cls = spe_diff_zy_cls
    """
    spe_diff_zy child of phase_child.
    """
    spe_diff_zz: spe_diff_zz_cls = spe_diff_zz_cls
    """
    spe_diff_zz child of phase_child.
    """
