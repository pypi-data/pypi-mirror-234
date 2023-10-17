#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .phase_9 import phase as phase_cls
from .geom_disable import geom_disable as geom_disable_cls
from .geom_dir_spec import geom_dir_spec as geom_dir_spec_cls
from .geom_dir_x import geom_dir_x as geom_dir_x_cls
from .geom_dir_y import geom_dir_y as geom_dir_y_cls
from .geom_dir_z import geom_dir_z as geom_dir_z_cls
from .geom_levels import geom_levels as geom_levels_cls
from .geom_bgthread import geom_bgthread as geom_bgthread_cls
from .open_channel import open_channel as open_channel_cls
from .inlet_number import inlet_number as inlet_number_cls
from .phase_spec import phase_spec as phase_spec_cls
from .ht_local import ht_local as ht_local_cls
from .ht_bottom import ht_bottom as ht_bottom_cls
from .den_spec import den_spec as den_spec_cls
from .frame_of_reference import frame_of_reference as frame_of_reference_cls
from .flow_spec import flow_spec as flow_spec_cls
from .mass_flow import mass_flow as mass_flow_cls
from .ec_mass_flow import ec_mass_flow as ec_mass_flow_cls
from .mass_flux import mass_flux as mass_flux_cls
from .mass_flux_ave import mass_flux_ave as mass_flux_ave_cls
from .tref import tref as tref_cls
from .pref import pref as pref_cls
from .upstream_torque import upstream_torque as upstream_torque_cls
from .upstream_t_enthalpy import upstream_t_enthalpy as upstream_t_enthalpy_cls
from .t0 import t0 as t0_cls
from .gauge_pressure import gauge_pressure as gauge_pressure_cls
from .direction_spec import direction_spec as direction_spec_cls
from .coordinate_system import coordinate_system as coordinate_system_cls
from .flow_direction import flow_direction as flow_direction_cls
from .direction_vector import direction_vector as direction_vector_cls
from .axis_direction_2 import axis_direction as axis_direction_cls
from .axis_origin_2 import axis_origin as axis_origin_cls
from .ke_spec import ke_spec as ke_spec_cls
from .nut import nut as nut_cls
from .kl import kl as kl_cls
from .intermit import intermit as intermit_cls
from .k import k as k_cls
from .e import e as e_cls
from .o import o as o_cls
from .v2 import v2 as v2_cls
from .turb_intensity import turb_intensity as turb_intensity_cls
from .turb_length_scale import turb_length_scale as turb_length_scale_cls
from .turb_hydraulic_diam import turb_hydraulic_diam as turb_hydraulic_diam_cls
from .turb_viscosity_ratio import turb_viscosity_ratio as turb_viscosity_ratio_cls
from .turb_viscosity_ratio_profile import turb_viscosity_ratio_profile as turb_viscosity_ratio_profile_cls
from .rst_spec import rst_spec as rst_spec_cls
from .uu import uu as uu_cls
from .vv import vv as vv_cls
from .ww import ww as ww_cls
from .uv import uv as uv_cls
from .vw import vw as vw_cls
from .uw import uw as uw_cls
from .ksgs_spec import ksgs_spec as ksgs_spec_cls
from .ksgs import ksgs as ksgs_cls
from .sgs_turb_intensity import sgs_turb_intensity as sgs_turb_intensity_cls
from .species_in_mole_fractions import species_in_mole_fractions as species_in_mole_fractions_cls
from .mf import mf as mf_cls
from .elec_potential_type import elec_potential_type as elec_potential_type_cls
from .potential_value import potential_value as potential_value_cls
from .dual_potential_type import dual_potential_type as dual_potential_type_cls
from .dual_potential_value import dual_potential_value as dual_potential_value_cls
from .x_displacement_type import x_displacement_type as x_displacement_type_cls
from .x_displacement_value import x_displacement_value as x_displacement_value_cls
from .y_displacement_type import y_displacement_type as y_displacement_type_cls
from .y_displacement_value import y_displacement_value as y_displacement_value_cls
from .z_displacement_type import z_displacement_type as z_displacement_type_cls
from .z_displacement_value import z_displacement_value as z_displacement_value_cls
from .prob_mode_1 import prob_mode_1 as prob_mode_1_cls
from .prob_mode_2 import prob_mode_2 as prob_mode_2_cls
from .prob_mode_3 import prob_mode_3 as prob_mode_3_cls
from .equ_required import equ_required as equ_required_cls
from .swirl_model import swirl_model as swirl_model_cls
from .swirl_factor import swirl_factor as swirl_factor_cls
from .fan_origin import fan_origin as fan_origin_cls
from .premixc import premixc as premixc_cls
from .premixc_var import premixc_var as premixc_var_cls
from .ecfm_sigma import ecfm_sigma as ecfm_sigma_cls
from .inert import inert as inert_cls
from .pollut_no import pollut_no as pollut_no_cls
from .pollut_hcn import pollut_hcn as pollut_hcn_cls
from .pollut_nh3 import pollut_nh3 as pollut_nh3_cls
from .pollut_n2o import pollut_n2o as pollut_n2o_cls
from .pollut_urea import pollut_urea as pollut_urea_cls
from .pollut_hnco import pollut_hnco as pollut_hnco_cls
from .pollut_nco import pollut_nco as pollut_nco_cls
from .pollut_so2 import pollut_so2 as pollut_so2_cls
from .pollut_h2s import pollut_h2s as pollut_h2s_cls
from .pollut_so3 import pollut_so3 as pollut_so3_cls
from .pollut_sh import pollut_sh as pollut_sh_cls
from .pollut_so import pollut_so as pollut_so_cls
from .pollut_soot import pollut_soot as pollut_soot_cls
from .pollut_nuclei import pollut_nuclei as pollut_nuclei_cls
from .pollut_ctar import pollut_ctar as pollut_ctar_cls
from .pollut_hg import pollut_hg as pollut_hg_cls
from .pollut_hgcl2 import pollut_hgcl2 as pollut_hgcl2_cls
from .pollut_hcl import pollut_hcl as pollut_hcl_cls
from .pollut_hgo import pollut_hgo as pollut_hgo_cls
from .pollut_cl import pollut_cl as pollut_cl_cls
from .pollut_cl2 import pollut_cl2 as pollut_cl2_cls
from .pollut_hgcl import pollut_hgcl as pollut_hgcl_cls
from .pollut_hocl import pollut_hocl as pollut_hocl_cls
from .fensapice_flow_bc_subtype import fensapice_flow_bc_subtype as fensapice_flow_bc_subtype_cls
from .fensapice_drop_bccustom import fensapice_drop_bccustom as fensapice_drop_bccustom_cls
from .fensapice_drop_lwc import fensapice_drop_lwc as fensapice_drop_lwc_cls
from .fensapice_drop_dtemp import fensapice_drop_dtemp as fensapice_drop_dtemp_cls
from .fensapice_drop_ddiam import fensapice_drop_ddiam as fensapice_drop_ddiam_cls
from .fensapice_drop_dv import fensapice_drop_dv as fensapice_drop_dv_cls
from .fensapice_drop_dx import fensapice_drop_dx as fensapice_drop_dx_cls
from .fensapice_drop_dy import fensapice_drop_dy as fensapice_drop_dy_cls
from .fensapice_drop_dz import fensapice_drop_dz as fensapice_drop_dz_cls
from .fensapice_dpm_surface_injection import fensapice_dpm_surface_injection as fensapice_dpm_surface_injection_cls
from .fensapice_dpm_inj_nstream import fensapice_dpm_inj_nstream as fensapice_dpm_inj_nstream_cls
from .fensapice_drop_icc import fensapice_drop_icc as fensapice_drop_icc_cls
from .fensapice_drop_ctemp import fensapice_drop_ctemp as fensapice_drop_ctemp_cls
from .fensapice_drop_cdiam import fensapice_drop_cdiam as fensapice_drop_cdiam_cls
from .fensapice_drop_cv import fensapice_drop_cv as fensapice_drop_cv_cls
from .fensapice_drop_cx import fensapice_drop_cx as fensapice_drop_cx_cls
from .fensapice_drop_cy import fensapice_drop_cy as fensapice_drop_cy_cls
from .fensapice_drop_cz import fensapice_drop_cz as fensapice_drop_cz_cls
from .fensapice_drop_vrh import fensapice_drop_vrh as fensapice_drop_vrh_cls
from .fensapice_drop_vrh_1 import fensapice_drop_vrh_1 as fensapice_drop_vrh_1_cls
from .fensapice_drop_vc import fensapice_drop_vc as fensapice_drop_vc_cls
from .radiation_bc import radiation_bc as radiation_bc_cls
from .radial_direction import radial_direction as radial_direction_cls
from .coll_dtheta import coll_dtheta as coll_dtheta_cls
from .coll_dphi import coll_dphi as coll_dphi_cls
from .band_q_irrad import band_q_irrad as band_q_irrad_cls
from .band_q_irrad_diffuse import band_q_irrad_diffuse as band_q_irrad_diffuse_cls
from .parallel_collimated_beam import parallel_collimated_beam as parallel_collimated_beam_cls
from .solar_direction import solar_direction as solar_direction_cls
from .solar_irradiation import solar_irradiation as solar_irradiation_cls
from .t_b_b_spec import t_b_b_spec as t_b_b_spec_cls
from .t_b_b import t_b_b as t_b_b_cls
from .in_emiss import in_emiss as in_emiss_cls
from .fmean import fmean as fmean_cls
from .fvar import fvar as fvar_cls
from .fmean2 import fmean2 as fmean2_cls
from .fvar2 import fvar2 as fvar2_cls
from .tss_scalar import tss_scalar as tss_scalar_cls
from .uds_bc import uds_bc as uds_bc_cls
from .uds import uds as uds_cls
from .pb_disc_bc import pb_disc_bc as pb_disc_bc_cls
from .pb_disc import pb_disc as pb_disc_cls
from .pb_qmom_bc import pb_qmom_bc as pb_qmom_bc_cls
from .pb_qmom import pb_qmom as pb_qmom_cls
from .pb_smm_bc import pb_smm_bc as pb_smm_bc_cls
from .pb_smm import pb_smm as pb_smm_cls
from .pb_dqmom_bc import pb_dqmom_bc as pb_dqmom_bc_cls
from .pb_dqmom import pb_dqmom as pb_dqmom_cls
from .dpm_bc_type import dpm_bc_type as dpm_bc_type_cls
from .dpm_bc_collision_partner import dpm_bc_collision_partner as dpm_bc_collision_partner_cls
from .reinj_inj import reinj_inj as reinj_inj_cls
from .dpm_bc_udf import dpm_bc_udf as dpm_bc_udf_cls
from .mixing_plane_thread import mixing_plane_thread as mixing_plane_thread_cls
from .wsf import wsf as wsf_cls
from .wsb import wsb as wsb_cls
from .wsn import wsn as wsn_cls
from .solar_fluxes import solar_fluxes as solar_fluxes_cls
from .solar_shining_factor import solar_shining_factor as solar_shining_factor_cls
from .radiating_s2s_surface import radiating_s2s_surface as radiating_s2s_surface_cls
from .slip_velocity import slip_velocity as slip_velocity_cls
from .velocity_ratio import velocity_ratio as velocity_ratio_cls
from .volume_frac import volume_frac as volume_frac_cls
from .granular_temperature import granular_temperature as granular_temperature_cls
from .iac import iac as iac_cls
from .ac_options import ac_options as ac_options_cls
from .impedance_0 import impedance_0 as impedance_0_cls
from .impedance_1 import impedance_1 as impedance_1_cls
from .impedance_2 import impedance_2 as impedance_2_cls
from .ac_wave import ac_wave as ac_wave_cls
class mass_flow_inlet_child(Group):
    """
    'child_object_type' of mass_flow_inlet.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['phase', 'geom_disable', 'geom_dir_spec', 'geom_dir_x', 'geom_dir_y',
         'geom_dir_z', 'geom_levels', 'geom_bgthread', 'open_channel',
         'inlet_number', 'phase_spec', 'ht_local', 'ht_bottom', 'den_spec',
         'frame_of_reference', 'flow_spec', 'mass_flow', 'ec_mass_flow',
         'mass_flux', 'mass_flux_ave', 'tref', 'pref', 'upstream_torque',
         'upstream_t_enthalpy', 't0', 'gauge_pressure', 'direction_spec',
         'coordinate_system', 'flow_direction', 'direction_vector',
         'axis_direction', 'axis_origin', 'ke_spec', 'nut', 'kl', 'intermit',
         'k', 'e', 'o', 'v2', 'turb_intensity', 'turb_length_scale',
         'turb_hydraulic_diam', 'turb_viscosity_ratio',
         'turb_viscosity_ratio_profile', 'rst_spec', 'uu', 'vv', 'ww', 'uv',
         'vw', 'uw', 'ksgs_spec', 'ksgs', 'sgs_turb_intensity',
         'species_in_mole_fractions', 'mf', 'elec_potential_type',
         'potential_value', 'dual_potential_type', 'dual_potential_value',
         'x_displacement_type', 'x_displacement_value', 'y_displacement_type',
         'y_displacement_value', 'z_displacement_type',
         'z_displacement_value', 'prob_mode_1', 'prob_mode_2', 'prob_mode_3',
         'equ_required', 'swirl_model', 'swirl_factor', 'fan_origin',
         'premixc', 'premixc_var', 'ecfm_sigma', 'inert', 'pollut_no',
         'pollut_hcn', 'pollut_nh3', 'pollut_n2o', 'pollut_urea',
         'pollut_hnco', 'pollut_nco', 'pollut_so2', 'pollut_h2s',
         'pollut_so3', 'pollut_sh', 'pollut_so', 'pollut_soot',
         'pollut_nuclei', 'pollut_ctar', 'pollut_hg', 'pollut_hgcl2',
         'pollut_hcl', 'pollut_hgo', 'pollut_cl', 'pollut_cl2', 'pollut_hgcl',
         'pollut_hocl', 'fensapice_flow_bc_subtype',
         'fensapice_drop_bccustom', 'fensapice_drop_lwc',
         'fensapice_drop_dtemp', 'fensapice_drop_ddiam', 'fensapice_drop_dv',
         'fensapice_drop_dx', 'fensapice_drop_dy', 'fensapice_drop_dz',
         'fensapice_dpm_surface_injection', 'fensapice_dpm_inj_nstream',
         'fensapice_drop_icc', 'fensapice_drop_ctemp', 'fensapice_drop_cdiam',
         'fensapice_drop_cv', 'fensapice_drop_cx', 'fensapice_drop_cy',
         'fensapice_drop_cz', 'fensapice_drop_vrh', 'fensapice_drop_vrh_1',
         'fensapice_drop_vc', 'radiation_bc', 'radial_direction',
         'coll_dtheta', 'coll_dphi', 'band_q_irrad', 'band_q_irrad_diffuse',
         'parallel_collimated_beam', 'solar_direction', 'solar_irradiation',
         't_b_b_spec', 't_b_b', 'in_emiss', 'fmean', 'fvar', 'fmean2',
         'fvar2', 'tss_scalar', 'uds_bc', 'uds', 'pb_disc_bc', 'pb_disc',
         'pb_qmom_bc', 'pb_qmom', 'pb_smm_bc', 'pb_smm', 'pb_dqmom_bc',
         'pb_dqmom', 'dpm_bc_type', 'dpm_bc_collision_partner', 'reinj_inj',
         'dpm_bc_udf', 'mixing_plane_thread', 'wsf', 'wsb', 'wsn',
         'solar_fluxes', 'solar_shining_factor', 'radiating_s2s_surface',
         'slip_velocity', 'velocity_ratio', 'volume_frac',
         'granular_temperature', 'iac', 'ac_options', 'impedance_0',
         'impedance_1', 'impedance_2', 'ac_wave']

    phase: phase_cls = phase_cls
    """
    phase child of mass_flow_inlet_child.
    """
    geom_disable: geom_disable_cls = geom_disable_cls
    """
    geom_disable child of mass_flow_inlet_child.
    """
    geom_dir_spec: geom_dir_spec_cls = geom_dir_spec_cls
    """
    geom_dir_spec child of mass_flow_inlet_child.
    """
    geom_dir_x: geom_dir_x_cls = geom_dir_x_cls
    """
    geom_dir_x child of mass_flow_inlet_child.
    """
    geom_dir_y: geom_dir_y_cls = geom_dir_y_cls
    """
    geom_dir_y child of mass_flow_inlet_child.
    """
    geom_dir_z: geom_dir_z_cls = geom_dir_z_cls
    """
    geom_dir_z child of mass_flow_inlet_child.
    """
    geom_levels: geom_levels_cls = geom_levels_cls
    """
    geom_levels child of mass_flow_inlet_child.
    """
    geom_bgthread: geom_bgthread_cls = geom_bgthread_cls
    """
    geom_bgthread child of mass_flow_inlet_child.
    """
    open_channel: open_channel_cls = open_channel_cls
    """
    open_channel child of mass_flow_inlet_child.
    """
    inlet_number: inlet_number_cls = inlet_number_cls
    """
    inlet_number child of mass_flow_inlet_child.
    """
    phase_spec: phase_spec_cls = phase_spec_cls
    """
    phase_spec child of mass_flow_inlet_child.
    """
    ht_local: ht_local_cls = ht_local_cls
    """
    ht_local child of mass_flow_inlet_child.
    """
    ht_bottom: ht_bottom_cls = ht_bottom_cls
    """
    ht_bottom child of mass_flow_inlet_child.
    """
    den_spec: den_spec_cls = den_spec_cls
    """
    den_spec child of mass_flow_inlet_child.
    """
    frame_of_reference: frame_of_reference_cls = frame_of_reference_cls
    """
    frame_of_reference child of mass_flow_inlet_child.
    """
    flow_spec: flow_spec_cls = flow_spec_cls
    """
    flow_spec child of mass_flow_inlet_child.
    """
    mass_flow: mass_flow_cls = mass_flow_cls
    """
    mass_flow child of mass_flow_inlet_child.
    """
    ec_mass_flow: ec_mass_flow_cls = ec_mass_flow_cls
    """
    ec_mass_flow child of mass_flow_inlet_child.
    """
    mass_flux: mass_flux_cls = mass_flux_cls
    """
    mass_flux child of mass_flow_inlet_child.
    """
    mass_flux_ave: mass_flux_ave_cls = mass_flux_ave_cls
    """
    mass_flux_ave child of mass_flow_inlet_child.
    """
    tref: tref_cls = tref_cls
    """
    tref child of mass_flow_inlet_child.
    """
    pref: pref_cls = pref_cls
    """
    pref child of mass_flow_inlet_child.
    """
    upstream_torque: upstream_torque_cls = upstream_torque_cls
    """
    upstream_torque child of mass_flow_inlet_child.
    """
    upstream_t_enthalpy: upstream_t_enthalpy_cls = upstream_t_enthalpy_cls
    """
    upstream_t_enthalpy child of mass_flow_inlet_child.
    """
    t0: t0_cls = t0_cls
    """
    t0 child of mass_flow_inlet_child.
    """
    gauge_pressure: gauge_pressure_cls = gauge_pressure_cls
    """
    gauge_pressure child of mass_flow_inlet_child.
    """
    direction_spec: direction_spec_cls = direction_spec_cls
    """
    direction_spec child of mass_flow_inlet_child.
    """
    coordinate_system: coordinate_system_cls = coordinate_system_cls
    """
    coordinate_system child of mass_flow_inlet_child.
    """
    flow_direction: flow_direction_cls = flow_direction_cls
    """
    flow_direction child of mass_flow_inlet_child.
    """
    direction_vector: direction_vector_cls = direction_vector_cls
    """
    direction_vector child of mass_flow_inlet_child.
    """
    axis_direction: axis_direction_cls = axis_direction_cls
    """
    axis_direction child of mass_flow_inlet_child.
    """
    axis_origin: axis_origin_cls = axis_origin_cls
    """
    axis_origin child of mass_flow_inlet_child.
    """
    ke_spec: ke_spec_cls = ke_spec_cls
    """
    ke_spec child of mass_flow_inlet_child.
    """
    nut: nut_cls = nut_cls
    """
    nut child of mass_flow_inlet_child.
    """
    kl: kl_cls = kl_cls
    """
    kl child of mass_flow_inlet_child.
    """
    intermit: intermit_cls = intermit_cls
    """
    intermit child of mass_flow_inlet_child.
    """
    k: k_cls = k_cls
    """
    k child of mass_flow_inlet_child.
    """
    e: e_cls = e_cls
    """
    e child of mass_flow_inlet_child.
    """
    o: o_cls = o_cls
    """
    o child of mass_flow_inlet_child.
    """
    v2: v2_cls = v2_cls
    """
    v2 child of mass_flow_inlet_child.
    """
    turb_intensity: turb_intensity_cls = turb_intensity_cls
    """
    turb_intensity child of mass_flow_inlet_child.
    """
    turb_length_scale: turb_length_scale_cls = turb_length_scale_cls
    """
    turb_length_scale child of mass_flow_inlet_child.
    """
    turb_hydraulic_diam: turb_hydraulic_diam_cls = turb_hydraulic_diam_cls
    """
    turb_hydraulic_diam child of mass_flow_inlet_child.
    """
    turb_viscosity_ratio: turb_viscosity_ratio_cls = turb_viscosity_ratio_cls
    """
    turb_viscosity_ratio child of mass_flow_inlet_child.
    """
    turb_viscosity_ratio_profile: turb_viscosity_ratio_profile_cls = turb_viscosity_ratio_profile_cls
    """
    turb_viscosity_ratio_profile child of mass_flow_inlet_child.
    """
    rst_spec: rst_spec_cls = rst_spec_cls
    """
    rst_spec child of mass_flow_inlet_child.
    """
    uu: uu_cls = uu_cls
    """
    uu child of mass_flow_inlet_child.
    """
    vv: vv_cls = vv_cls
    """
    vv child of mass_flow_inlet_child.
    """
    ww: ww_cls = ww_cls
    """
    ww child of mass_flow_inlet_child.
    """
    uv: uv_cls = uv_cls
    """
    uv child of mass_flow_inlet_child.
    """
    vw: vw_cls = vw_cls
    """
    vw child of mass_flow_inlet_child.
    """
    uw: uw_cls = uw_cls
    """
    uw child of mass_flow_inlet_child.
    """
    ksgs_spec: ksgs_spec_cls = ksgs_spec_cls
    """
    ksgs_spec child of mass_flow_inlet_child.
    """
    ksgs: ksgs_cls = ksgs_cls
    """
    ksgs child of mass_flow_inlet_child.
    """
    sgs_turb_intensity: sgs_turb_intensity_cls = sgs_turb_intensity_cls
    """
    sgs_turb_intensity child of mass_flow_inlet_child.
    """
    species_in_mole_fractions: species_in_mole_fractions_cls = species_in_mole_fractions_cls
    """
    species_in_mole_fractions child of mass_flow_inlet_child.
    """
    mf: mf_cls = mf_cls
    """
    mf child of mass_flow_inlet_child.
    """
    elec_potential_type: elec_potential_type_cls = elec_potential_type_cls
    """
    elec_potential_type child of mass_flow_inlet_child.
    """
    potential_value: potential_value_cls = potential_value_cls
    """
    potential_value child of mass_flow_inlet_child.
    """
    dual_potential_type: dual_potential_type_cls = dual_potential_type_cls
    """
    dual_potential_type child of mass_flow_inlet_child.
    """
    dual_potential_value: dual_potential_value_cls = dual_potential_value_cls
    """
    dual_potential_value child of mass_flow_inlet_child.
    """
    x_displacement_type: x_displacement_type_cls = x_displacement_type_cls
    """
    x_displacement_type child of mass_flow_inlet_child.
    """
    x_displacement_value: x_displacement_value_cls = x_displacement_value_cls
    """
    x_displacement_value child of mass_flow_inlet_child.
    """
    y_displacement_type: y_displacement_type_cls = y_displacement_type_cls
    """
    y_displacement_type child of mass_flow_inlet_child.
    """
    y_displacement_value: y_displacement_value_cls = y_displacement_value_cls
    """
    y_displacement_value child of mass_flow_inlet_child.
    """
    z_displacement_type: z_displacement_type_cls = z_displacement_type_cls
    """
    z_displacement_type child of mass_flow_inlet_child.
    """
    z_displacement_value: z_displacement_value_cls = z_displacement_value_cls
    """
    z_displacement_value child of mass_flow_inlet_child.
    """
    prob_mode_1: prob_mode_1_cls = prob_mode_1_cls
    """
    prob_mode_1 child of mass_flow_inlet_child.
    """
    prob_mode_2: prob_mode_2_cls = prob_mode_2_cls
    """
    prob_mode_2 child of mass_flow_inlet_child.
    """
    prob_mode_3: prob_mode_3_cls = prob_mode_3_cls
    """
    prob_mode_3 child of mass_flow_inlet_child.
    """
    equ_required: equ_required_cls = equ_required_cls
    """
    equ_required child of mass_flow_inlet_child.
    """
    swirl_model: swirl_model_cls = swirl_model_cls
    """
    swirl_model child of mass_flow_inlet_child.
    """
    swirl_factor: swirl_factor_cls = swirl_factor_cls
    """
    swirl_factor child of mass_flow_inlet_child.
    """
    fan_origin: fan_origin_cls = fan_origin_cls
    """
    fan_origin child of mass_flow_inlet_child.
    """
    premixc: premixc_cls = premixc_cls
    """
    premixc child of mass_flow_inlet_child.
    """
    premixc_var: premixc_var_cls = premixc_var_cls
    """
    premixc_var child of mass_flow_inlet_child.
    """
    ecfm_sigma: ecfm_sigma_cls = ecfm_sigma_cls
    """
    ecfm_sigma child of mass_flow_inlet_child.
    """
    inert: inert_cls = inert_cls
    """
    inert child of mass_flow_inlet_child.
    """
    pollut_no: pollut_no_cls = pollut_no_cls
    """
    pollut_no child of mass_flow_inlet_child.
    """
    pollut_hcn: pollut_hcn_cls = pollut_hcn_cls
    """
    pollut_hcn child of mass_flow_inlet_child.
    """
    pollut_nh3: pollut_nh3_cls = pollut_nh3_cls
    """
    pollut_nh3 child of mass_flow_inlet_child.
    """
    pollut_n2o: pollut_n2o_cls = pollut_n2o_cls
    """
    pollut_n2o child of mass_flow_inlet_child.
    """
    pollut_urea: pollut_urea_cls = pollut_urea_cls
    """
    pollut_urea child of mass_flow_inlet_child.
    """
    pollut_hnco: pollut_hnco_cls = pollut_hnco_cls
    """
    pollut_hnco child of mass_flow_inlet_child.
    """
    pollut_nco: pollut_nco_cls = pollut_nco_cls
    """
    pollut_nco child of mass_flow_inlet_child.
    """
    pollut_so2: pollut_so2_cls = pollut_so2_cls
    """
    pollut_so2 child of mass_flow_inlet_child.
    """
    pollut_h2s: pollut_h2s_cls = pollut_h2s_cls
    """
    pollut_h2s child of mass_flow_inlet_child.
    """
    pollut_so3: pollut_so3_cls = pollut_so3_cls
    """
    pollut_so3 child of mass_flow_inlet_child.
    """
    pollut_sh: pollut_sh_cls = pollut_sh_cls
    """
    pollut_sh child of mass_flow_inlet_child.
    """
    pollut_so: pollut_so_cls = pollut_so_cls
    """
    pollut_so child of mass_flow_inlet_child.
    """
    pollut_soot: pollut_soot_cls = pollut_soot_cls
    """
    pollut_soot child of mass_flow_inlet_child.
    """
    pollut_nuclei: pollut_nuclei_cls = pollut_nuclei_cls
    """
    pollut_nuclei child of mass_flow_inlet_child.
    """
    pollut_ctar: pollut_ctar_cls = pollut_ctar_cls
    """
    pollut_ctar child of mass_flow_inlet_child.
    """
    pollut_hg: pollut_hg_cls = pollut_hg_cls
    """
    pollut_hg child of mass_flow_inlet_child.
    """
    pollut_hgcl2: pollut_hgcl2_cls = pollut_hgcl2_cls
    """
    pollut_hgcl2 child of mass_flow_inlet_child.
    """
    pollut_hcl: pollut_hcl_cls = pollut_hcl_cls
    """
    pollut_hcl child of mass_flow_inlet_child.
    """
    pollut_hgo: pollut_hgo_cls = pollut_hgo_cls
    """
    pollut_hgo child of mass_flow_inlet_child.
    """
    pollut_cl: pollut_cl_cls = pollut_cl_cls
    """
    pollut_cl child of mass_flow_inlet_child.
    """
    pollut_cl2: pollut_cl2_cls = pollut_cl2_cls
    """
    pollut_cl2 child of mass_flow_inlet_child.
    """
    pollut_hgcl: pollut_hgcl_cls = pollut_hgcl_cls
    """
    pollut_hgcl child of mass_flow_inlet_child.
    """
    pollut_hocl: pollut_hocl_cls = pollut_hocl_cls
    """
    pollut_hocl child of mass_flow_inlet_child.
    """
    fensapice_flow_bc_subtype: fensapice_flow_bc_subtype_cls = fensapice_flow_bc_subtype_cls
    """
    fensapice_flow_bc_subtype child of mass_flow_inlet_child.
    """
    fensapice_drop_bccustom: fensapice_drop_bccustom_cls = fensapice_drop_bccustom_cls
    """
    fensapice_drop_bccustom child of mass_flow_inlet_child.
    """
    fensapice_drop_lwc: fensapice_drop_lwc_cls = fensapice_drop_lwc_cls
    """
    fensapice_drop_lwc child of mass_flow_inlet_child.
    """
    fensapice_drop_dtemp: fensapice_drop_dtemp_cls = fensapice_drop_dtemp_cls
    """
    fensapice_drop_dtemp child of mass_flow_inlet_child.
    """
    fensapice_drop_ddiam: fensapice_drop_ddiam_cls = fensapice_drop_ddiam_cls
    """
    fensapice_drop_ddiam child of mass_flow_inlet_child.
    """
    fensapice_drop_dv: fensapice_drop_dv_cls = fensapice_drop_dv_cls
    """
    fensapice_drop_dv child of mass_flow_inlet_child.
    """
    fensapice_drop_dx: fensapice_drop_dx_cls = fensapice_drop_dx_cls
    """
    fensapice_drop_dx child of mass_flow_inlet_child.
    """
    fensapice_drop_dy: fensapice_drop_dy_cls = fensapice_drop_dy_cls
    """
    fensapice_drop_dy child of mass_flow_inlet_child.
    """
    fensapice_drop_dz: fensapice_drop_dz_cls = fensapice_drop_dz_cls
    """
    fensapice_drop_dz child of mass_flow_inlet_child.
    """
    fensapice_dpm_surface_injection: fensapice_dpm_surface_injection_cls = fensapice_dpm_surface_injection_cls
    """
    fensapice_dpm_surface_injection child of mass_flow_inlet_child.
    """
    fensapice_dpm_inj_nstream: fensapice_dpm_inj_nstream_cls = fensapice_dpm_inj_nstream_cls
    """
    fensapice_dpm_inj_nstream child of mass_flow_inlet_child.
    """
    fensapice_drop_icc: fensapice_drop_icc_cls = fensapice_drop_icc_cls
    """
    fensapice_drop_icc child of mass_flow_inlet_child.
    """
    fensapice_drop_ctemp: fensapice_drop_ctemp_cls = fensapice_drop_ctemp_cls
    """
    fensapice_drop_ctemp child of mass_flow_inlet_child.
    """
    fensapice_drop_cdiam: fensapice_drop_cdiam_cls = fensapice_drop_cdiam_cls
    """
    fensapice_drop_cdiam child of mass_flow_inlet_child.
    """
    fensapice_drop_cv: fensapice_drop_cv_cls = fensapice_drop_cv_cls
    """
    fensapice_drop_cv child of mass_flow_inlet_child.
    """
    fensapice_drop_cx: fensapice_drop_cx_cls = fensapice_drop_cx_cls
    """
    fensapice_drop_cx child of mass_flow_inlet_child.
    """
    fensapice_drop_cy: fensapice_drop_cy_cls = fensapice_drop_cy_cls
    """
    fensapice_drop_cy child of mass_flow_inlet_child.
    """
    fensapice_drop_cz: fensapice_drop_cz_cls = fensapice_drop_cz_cls
    """
    fensapice_drop_cz child of mass_flow_inlet_child.
    """
    fensapice_drop_vrh: fensapice_drop_vrh_cls = fensapice_drop_vrh_cls
    """
    fensapice_drop_vrh child of mass_flow_inlet_child.
    """
    fensapice_drop_vrh_1: fensapice_drop_vrh_1_cls = fensapice_drop_vrh_1_cls
    """
    fensapice_drop_vrh_1 child of mass_flow_inlet_child.
    """
    fensapice_drop_vc: fensapice_drop_vc_cls = fensapice_drop_vc_cls
    """
    fensapice_drop_vc child of mass_flow_inlet_child.
    """
    radiation_bc: radiation_bc_cls = radiation_bc_cls
    """
    radiation_bc child of mass_flow_inlet_child.
    """
    radial_direction: radial_direction_cls = radial_direction_cls
    """
    radial_direction child of mass_flow_inlet_child.
    """
    coll_dtheta: coll_dtheta_cls = coll_dtheta_cls
    """
    coll_dtheta child of mass_flow_inlet_child.
    """
    coll_dphi: coll_dphi_cls = coll_dphi_cls
    """
    coll_dphi child of mass_flow_inlet_child.
    """
    band_q_irrad: band_q_irrad_cls = band_q_irrad_cls
    """
    band_q_irrad child of mass_flow_inlet_child.
    """
    band_q_irrad_diffuse: band_q_irrad_diffuse_cls = band_q_irrad_diffuse_cls
    """
    band_q_irrad_diffuse child of mass_flow_inlet_child.
    """
    parallel_collimated_beam: parallel_collimated_beam_cls = parallel_collimated_beam_cls
    """
    parallel_collimated_beam child of mass_flow_inlet_child.
    """
    solar_direction: solar_direction_cls = solar_direction_cls
    """
    solar_direction child of mass_flow_inlet_child.
    """
    solar_irradiation: solar_irradiation_cls = solar_irradiation_cls
    """
    solar_irradiation child of mass_flow_inlet_child.
    """
    t_b_b_spec: t_b_b_spec_cls = t_b_b_spec_cls
    """
    t_b_b_spec child of mass_flow_inlet_child.
    """
    t_b_b: t_b_b_cls = t_b_b_cls
    """
    t_b_b child of mass_flow_inlet_child.
    """
    in_emiss: in_emiss_cls = in_emiss_cls
    """
    in_emiss child of mass_flow_inlet_child.
    """
    fmean: fmean_cls = fmean_cls
    """
    fmean child of mass_flow_inlet_child.
    """
    fvar: fvar_cls = fvar_cls
    """
    fvar child of mass_flow_inlet_child.
    """
    fmean2: fmean2_cls = fmean2_cls
    """
    fmean2 child of mass_flow_inlet_child.
    """
    fvar2: fvar2_cls = fvar2_cls
    """
    fvar2 child of mass_flow_inlet_child.
    """
    tss_scalar: tss_scalar_cls = tss_scalar_cls
    """
    tss_scalar child of mass_flow_inlet_child.
    """
    uds_bc: uds_bc_cls = uds_bc_cls
    """
    uds_bc child of mass_flow_inlet_child.
    """
    uds: uds_cls = uds_cls
    """
    uds child of mass_flow_inlet_child.
    """
    pb_disc_bc: pb_disc_bc_cls = pb_disc_bc_cls
    """
    pb_disc_bc child of mass_flow_inlet_child.
    """
    pb_disc: pb_disc_cls = pb_disc_cls
    """
    pb_disc child of mass_flow_inlet_child.
    """
    pb_qmom_bc: pb_qmom_bc_cls = pb_qmom_bc_cls
    """
    pb_qmom_bc child of mass_flow_inlet_child.
    """
    pb_qmom: pb_qmom_cls = pb_qmom_cls
    """
    pb_qmom child of mass_flow_inlet_child.
    """
    pb_smm_bc: pb_smm_bc_cls = pb_smm_bc_cls
    """
    pb_smm_bc child of mass_flow_inlet_child.
    """
    pb_smm: pb_smm_cls = pb_smm_cls
    """
    pb_smm child of mass_flow_inlet_child.
    """
    pb_dqmom_bc: pb_dqmom_bc_cls = pb_dqmom_bc_cls
    """
    pb_dqmom_bc child of mass_flow_inlet_child.
    """
    pb_dqmom: pb_dqmom_cls = pb_dqmom_cls
    """
    pb_dqmom child of mass_flow_inlet_child.
    """
    dpm_bc_type: dpm_bc_type_cls = dpm_bc_type_cls
    """
    dpm_bc_type child of mass_flow_inlet_child.
    """
    dpm_bc_collision_partner: dpm_bc_collision_partner_cls = dpm_bc_collision_partner_cls
    """
    dpm_bc_collision_partner child of mass_flow_inlet_child.
    """
    reinj_inj: reinj_inj_cls = reinj_inj_cls
    """
    reinj_inj child of mass_flow_inlet_child.
    """
    dpm_bc_udf: dpm_bc_udf_cls = dpm_bc_udf_cls
    """
    dpm_bc_udf child of mass_flow_inlet_child.
    """
    mixing_plane_thread: mixing_plane_thread_cls = mixing_plane_thread_cls
    """
    mixing_plane_thread child of mass_flow_inlet_child.
    """
    wsf: wsf_cls = wsf_cls
    """
    wsf child of mass_flow_inlet_child.
    """
    wsb: wsb_cls = wsb_cls
    """
    wsb child of mass_flow_inlet_child.
    """
    wsn: wsn_cls = wsn_cls
    """
    wsn child of mass_flow_inlet_child.
    """
    solar_fluxes: solar_fluxes_cls = solar_fluxes_cls
    """
    solar_fluxes child of mass_flow_inlet_child.
    """
    solar_shining_factor: solar_shining_factor_cls = solar_shining_factor_cls
    """
    solar_shining_factor child of mass_flow_inlet_child.
    """
    radiating_s2s_surface: radiating_s2s_surface_cls = radiating_s2s_surface_cls
    """
    radiating_s2s_surface child of mass_flow_inlet_child.
    """
    slip_velocity: slip_velocity_cls = slip_velocity_cls
    """
    slip_velocity child of mass_flow_inlet_child.
    """
    velocity_ratio: velocity_ratio_cls = velocity_ratio_cls
    """
    velocity_ratio child of mass_flow_inlet_child.
    """
    volume_frac: volume_frac_cls = volume_frac_cls
    """
    volume_frac child of mass_flow_inlet_child.
    """
    granular_temperature: granular_temperature_cls = granular_temperature_cls
    """
    granular_temperature child of mass_flow_inlet_child.
    """
    iac: iac_cls = iac_cls
    """
    iac child of mass_flow_inlet_child.
    """
    ac_options: ac_options_cls = ac_options_cls
    """
    ac_options child of mass_flow_inlet_child.
    """
    impedance_0: impedance_0_cls = impedance_0_cls
    """
    impedance_0 child of mass_flow_inlet_child.
    """
    impedance_1: impedance_1_cls = impedance_1_cls
    """
    impedance_1 child of mass_flow_inlet_child.
    """
    impedance_2: impedance_2_cls = impedance_2_cls
    """
    impedance_2 child of mass_flow_inlet_child.
    """
    ac_wave: ac_wave_cls = ac_wave_cls
    """
    ac_wave child of mass_flow_inlet_child.
    """
