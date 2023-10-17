#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .phase_16 import phase as phase_cls
from .geom_disable import geom_disable as geom_disable_cls
from .geom_dir_spec import geom_dir_spec as geom_dir_spec_cls
from .geom_dir_x import geom_dir_x as geom_dir_x_cls
from .geom_dir_y import geom_dir_y as geom_dir_y_cls
from .geom_dir_z import geom_dir_z as geom_dir_z_cls
from .geom_levels import geom_levels as geom_levels_cls
from .geom_bgthread import geom_bgthread as geom_bgthread_cls
from .p import p as p_cls
from .m import m as m_cls
from .t import t as t_cls
from .non_equil_boundary import non_equil_boundary as non_equil_boundary_cls
from .tve import tve as tve_cls
from .coordinate_system import coordinate_system as coordinate_system_cls
from .ni_1 import ni as ni_cls
from .nj_1 import nj as nj_cls
from .nk_1 import nk as nk_cls
from .flow_direction_component import flow_direction_component as flow_direction_component_cls
from .axis_direction_component_1 import axis_direction_component as axis_direction_component_cls
from .axis_origin_component_1 import axis_origin_component as axis_origin_component_cls
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
from .radiation_bc import radiation_bc as radiation_bc_cls
from .radial_direction_component import radial_direction_component as radial_direction_component_cls
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
from .uds_bc import uds_bc as uds_bc_cls
from .uds import uds as uds_cls
from .dpm_bc_type import dpm_bc_type as dpm_bc_type_cls
from .dpm_bc_collision_partner import dpm_bc_collision_partner as dpm_bc_collision_partner_cls
from .reinj_inj import reinj_inj as reinj_inj_cls
from .dpm_bc_udf import dpm_bc_udf as dpm_bc_udf_cls
from .solar_fluxes import solar_fluxes as solar_fluxes_cls
from .solar_shining_factor import solar_shining_factor as solar_shining_factor_cls
from .radiating_s2s_surface import radiating_s2s_surface as radiating_s2s_surface_cls
class pressure_far_field_child(Group):
    """
    'child_object_type' of pressure_far_field.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['phase', 'geom_disable', 'geom_dir_spec', 'geom_dir_x', 'geom_dir_y',
         'geom_dir_z', 'geom_levels', 'geom_bgthread', 'p', 'm', 't',
         'non_equil_boundary', 'tve', 'coordinate_system', 'ni', 'nj', 'nk',
         'flow_direction_component', 'axis_direction_component',
         'axis_origin_component', 'ke_spec', 'nut', 'kl', 'intermit', 'k',
         'e', 'o', 'v2', 'turb_intensity', 'turb_length_scale',
         'turb_hydraulic_diam', 'turb_viscosity_ratio',
         'turb_viscosity_ratio_profile', 'rst_spec', 'uu', 'vv', 'ww', 'uv',
         'vw', 'uw', 'ksgs_spec', 'ksgs', 'sgs_turb_intensity',
         'radiation_bc', 'radial_direction_component', 'coll_dtheta',
         'coll_dphi', 'band_q_irrad', 'band_q_irrad_diffuse',
         'parallel_collimated_beam', 'solar_direction', 'solar_irradiation',
         't_b_b_spec', 't_b_b', 'in_emiss', 'fmean', 'fvar', 'fmean2',
         'fvar2', 'species_in_mole_fractions', 'mf', 'elec_potential_type',
         'potential_value', 'dual_potential_type', 'dual_potential_value',
         'x_displacement_type', 'x_displacement_value', 'y_displacement_type',
         'y_displacement_value', 'z_displacement_type',
         'z_displacement_value', 'prob_mode_1', 'prob_mode_2', 'prob_mode_3',
         'pollut_no', 'pollut_hcn', 'pollut_nh3', 'pollut_n2o', 'pollut_urea',
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
         'fensapice_drop_vc', 'uds_bc', 'uds', 'dpm_bc_type',
         'dpm_bc_collision_partner', 'reinj_inj', 'dpm_bc_udf',
         'solar_fluxes', 'solar_shining_factor', 'radiating_s2s_surface']

    phase: phase_cls = phase_cls
    """
    phase child of pressure_far_field_child.
    """
    geom_disable: geom_disable_cls = geom_disable_cls
    """
    geom_disable child of pressure_far_field_child.
    """
    geom_dir_spec: geom_dir_spec_cls = geom_dir_spec_cls
    """
    geom_dir_spec child of pressure_far_field_child.
    """
    geom_dir_x: geom_dir_x_cls = geom_dir_x_cls
    """
    geom_dir_x child of pressure_far_field_child.
    """
    geom_dir_y: geom_dir_y_cls = geom_dir_y_cls
    """
    geom_dir_y child of pressure_far_field_child.
    """
    geom_dir_z: geom_dir_z_cls = geom_dir_z_cls
    """
    geom_dir_z child of pressure_far_field_child.
    """
    geom_levels: geom_levels_cls = geom_levels_cls
    """
    geom_levels child of pressure_far_field_child.
    """
    geom_bgthread: geom_bgthread_cls = geom_bgthread_cls
    """
    geom_bgthread child of pressure_far_field_child.
    """
    p: p_cls = p_cls
    """
    p child of pressure_far_field_child.
    """
    m: m_cls = m_cls
    """
    m child of pressure_far_field_child.
    """
    t: t_cls = t_cls
    """
    t child of pressure_far_field_child.
    """
    non_equil_boundary: non_equil_boundary_cls = non_equil_boundary_cls
    """
    non_equil_boundary child of pressure_far_field_child.
    """
    tve: tve_cls = tve_cls
    """
    tve child of pressure_far_field_child.
    """
    coordinate_system: coordinate_system_cls = coordinate_system_cls
    """
    coordinate_system child of pressure_far_field_child.
    """
    ni: ni_cls = ni_cls
    """
    ni child of pressure_far_field_child.
    """
    nj: nj_cls = nj_cls
    """
    nj child of pressure_far_field_child.
    """
    nk: nk_cls = nk_cls
    """
    nk child of pressure_far_field_child.
    """
    flow_direction_component: flow_direction_component_cls = flow_direction_component_cls
    """
    flow_direction_component child of pressure_far_field_child.
    """
    axis_direction_component: axis_direction_component_cls = axis_direction_component_cls
    """
    axis_direction_component child of pressure_far_field_child.
    """
    axis_origin_component: axis_origin_component_cls = axis_origin_component_cls
    """
    axis_origin_component child of pressure_far_field_child.
    """
    ke_spec: ke_spec_cls = ke_spec_cls
    """
    ke_spec child of pressure_far_field_child.
    """
    nut: nut_cls = nut_cls
    """
    nut child of pressure_far_field_child.
    """
    kl: kl_cls = kl_cls
    """
    kl child of pressure_far_field_child.
    """
    intermit: intermit_cls = intermit_cls
    """
    intermit child of pressure_far_field_child.
    """
    k: k_cls = k_cls
    """
    k child of pressure_far_field_child.
    """
    e: e_cls = e_cls
    """
    e child of pressure_far_field_child.
    """
    o: o_cls = o_cls
    """
    o child of pressure_far_field_child.
    """
    v2: v2_cls = v2_cls
    """
    v2 child of pressure_far_field_child.
    """
    turb_intensity: turb_intensity_cls = turb_intensity_cls
    """
    turb_intensity child of pressure_far_field_child.
    """
    turb_length_scale: turb_length_scale_cls = turb_length_scale_cls
    """
    turb_length_scale child of pressure_far_field_child.
    """
    turb_hydraulic_diam: turb_hydraulic_diam_cls = turb_hydraulic_diam_cls
    """
    turb_hydraulic_diam child of pressure_far_field_child.
    """
    turb_viscosity_ratio: turb_viscosity_ratio_cls = turb_viscosity_ratio_cls
    """
    turb_viscosity_ratio child of pressure_far_field_child.
    """
    turb_viscosity_ratio_profile: turb_viscosity_ratio_profile_cls = turb_viscosity_ratio_profile_cls
    """
    turb_viscosity_ratio_profile child of pressure_far_field_child.
    """
    rst_spec: rst_spec_cls = rst_spec_cls
    """
    rst_spec child of pressure_far_field_child.
    """
    uu: uu_cls = uu_cls
    """
    uu child of pressure_far_field_child.
    """
    vv: vv_cls = vv_cls
    """
    vv child of pressure_far_field_child.
    """
    ww: ww_cls = ww_cls
    """
    ww child of pressure_far_field_child.
    """
    uv: uv_cls = uv_cls
    """
    uv child of pressure_far_field_child.
    """
    vw: vw_cls = vw_cls
    """
    vw child of pressure_far_field_child.
    """
    uw: uw_cls = uw_cls
    """
    uw child of pressure_far_field_child.
    """
    ksgs_spec: ksgs_spec_cls = ksgs_spec_cls
    """
    ksgs_spec child of pressure_far_field_child.
    """
    ksgs: ksgs_cls = ksgs_cls
    """
    ksgs child of pressure_far_field_child.
    """
    sgs_turb_intensity: sgs_turb_intensity_cls = sgs_turb_intensity_cls
    """
    sgs_turb_intensity child of pressure_far_field_child.
    """
    radiation_bc: radiation_bc_cls = radiation_bc_cls
    """
    radiation_bc child of pressure_far_field_child.
    """
    radial_direction_component: radial_direction_component_cls = radial_direction_component_cls
    """
    radial_direction_component child of pressure_far_field_child.
    """
    coll_dtheta: coll_dtheta_cls = coll_dtheta_cls
    """
    coll_dtheta child of pressure_far_field_child.
    """
    coll_dphi: coll_dphi_cls = coll_dphi_cls
    """
    coll_dphi child of pressure_far_field_child.
    """
    band_q_irrad: band_q_irrad_cls = band_q_irrad_cls
    """
    band_q_irrad child of pressure_far_field_child.
    """
    band_q_irrad_diffuse: band_q_irrad_diffuse_cls = band_q_irrad_diffuse_cls
    """
    band_q_irrad_diffuse child of pressure_far_field_child.
    """
    parallel_collimated_beam: parallel_collimated_beam_cls = parallel_collimated_beam_cls
    """
    parallel_collimated_beam child of pressure_far_field_child.
    """
    solar_direction: solar_direction_cls = solar_direction_cls
    """
    solar_direction child of pressure_far_field_child.
    """
    solar_irradiation: solar_irradiation_cls = solar_irradiation_cls
    """
    solar_irradiation child of pressure_far_field_child.
    """
    t_b_b_spec: t_b_b_spec_cls = t_b_b_spec_cls
    """
    t_b_b_spec child of pressure_far_field_child.
    """
    t_b_b: t_b_b_cls = t_b_b_cls
    """
    t_b_b child of pressure_far_field_child.
    """
    in_emiss: in_emiss_cls = in_emiss_cls
    """
    in_emiss child of pressure_far_field_child.
    """
    fmean: fmean_cls = fmean_cls
    """
    fmean child of pressure_far_field_child.
    """
    fvar: fvar_cls = fvar_cls
    """
    fvar child of pressure_far_field_child.
    """
    fmean2: fmean2_cls = fmean2_cls
    """
    fmean2 child of pressure_far_field_child.
    """
    fvar2: fvar2_cls = fvar2_cls
    """
    fvar2 child of pressure_far_field_child.
    """
    species_in_mole_fractions: species_in_mole_fractions_cls = species_in_mole_fractions_cls
    """
    species_in_mole_fractions child of pressure_far_field_child.
    """
    mf: mf_cls = mf_cls
    """
    mf child of pressure_far_field_child.
    """
    elec_potential_type: elec_potential_type_cls = elec_potential_type_cls
    """
    elec_potential_type child of pressure_far_field_child.
    """
    potential_value: potential_value_cls = potential_value_cls
    """
    potential_value child of pressure_far_field_child.
    """
    dual_potential_type: dual_potential_type_cls = dual_potential_type_cls
    """
    dual_potential_type child of pressure_far_field_child.
    """
    dual_potential_value: dual_potential_value_cls = dual_potential_value_cls
    """
    dual_potential_value child of pressure_far_field_child.
    """
    x_displacement_type: x_displacement_type_cls = x_displacement_type_cls
    """
    x_displacement_type child of pressure_far_field_child.
    """
    x_displacement_value: x_displacement_value_cls = x_displacement_value_cls
    """
    x_displacement_value child of pressure_far_field_child.
    """
    y_displacement_type: y_displacement_type_cls = y_displacement_type_cls
    """
    y_displacement_type child of pressure_far_field_child.
    """
    y_displacement_value: y_displacement_value_cls = y_displacement_value_cls
    """
    y_displacement_value child of pressure_far_field_child.
    """
    z_displacement_type: z_displacement_type_cls = z_displacement_type_cls
    """
    z_displacement_type child of pressure_far_field_child.
    """
    z_displacement_value: z_displacement_value_cls = z_displacement_value_cls
    """
    z_displacement_value child of pressure_far_field_child.
    """
    prob_mode_1: prob_mode_1_cls = prob_mode_1_cls
    """
    prob_mode_1 child of pressure_far_field_child.
    """
    prob_mode_2: prob_mode_2_cls = prob_mode_2_cls
    """
    prob_mode_2 child of pressure_far_field_child.
    """
    prob_mode_3: prob_mode_3_cls = prob_mode_3_cls
    """
    prob_mode_3 child of pressure_far_field_child.
    """
    pollut_no: pollut_no_cls = pollut_no_cls
    """
    pollut_no child of pressure_far_field_child.
    """
    pollut_hcn: pollut_hcn_cls = pollut_hcn_cls
    """
    pollut_hcn child of pressure_far_field_child.
    """
    pollut_nh3: pollut_nh3_cls = pollut_nh3_cls
    """
    pollut_nh3 child of pressure_far_field_child.
    """
    pollut_n2o: pollut_n2o_cls = pollut_n2o_cls
    """
    pollut_n2o child of pressure_far_field_child.
    """
    pollut_urea: pollut_urea_cls = pollut_urea_cls
    """
    pollut_urea child of pressure_far_field_child.
    """
    pollut_hnco: pollut_hnco_cls = pollut_hnco_cls
    """
    pollut_hnco child of pressure_far_field_child.
    """
    pollut_nco: pollut_nco_cls = pollut_nco_cls
    """
    pollut_nco child of pressure_far_field_child.
    """
    pollut_so2: pollut_so2_cls = pollut_so2_cls
    """
    pollut_so2 child of pressure_far_field_child.
    """
    pollut_h2s: pollut_h2s_cls = pollut_h2s_cls
    """
    pollut_h2s child of pressure_far_field_child.
    """
    pollut_so3: pollut_so3_cls = pollut_so3_cls
    """
    pollut_so3 child of pressure_far_field_child.
    """
    pollut_sh: pollut_sh_cls = pollut_sh_cls
    """
    pollut_sh child of pressure_far_field_child.
    """
    pollut_so: pollut_so_cls = pollut_so_cls
    """
    pollut_so child of pressure_far_field_child.
    """
    pollut_soot: pollut_soot_cls = pollut_soot_cls
    """
    pollut_soot child of pressure_far_field_child.
    """
    pollut_nuclei: pollut_nuclei_cls = pollut_nuclei_cls
    """
    pollut_nuclei child of pressure_far_field_child.
    """
    pollut_ctar: pollut_ctar_cls = pollut_ctar_cls
    """
    pollut_ctar child of pressure_far_field_child.
    """
    pollut_hg: pollut_hg_cls = pollut_hg_cls
    """
    pollut_hg child of pressure_far_field_child.
    """
    pollut_hgcl2: pollut_hgcl2_cls = pollut_hgcl2_cls
    """
    pollut_hgcl2 child of pressure_far_field_child.
    """
    pollut_hcl: pollut_hcl_cls = pollut_hcl_cls
    """
    pollut_hcl child of pressure_far_field_child.
    """
    pollut_hgo: pollut_hgo_cls = pollut_hgo_cls
    """
    pollut_hgo child of pressure_far_field_child.
    """
    pollut_cl: pollut_cl_cls = pollut_cl_cls
    """
    pollut_cl child of pressure_far_field_child.
    """
    pollut_cl2: pollut_cl2_cls = pollut_cl2_cls
    """
    pollut_cl2 child of pressure_far_field_child.
    """
    pollut_hgcl: pollut_hgcl_cls = pollut_hgcl_cls
    """
    pollut_hgcl child of pressure_far_field_child.
    """
    pollut_hocl: pollut_hocl_cls = pollut_hocl_cls
    """
    pollut_hocl child of pressure_far_field_child.
    """
    fensapice_flow_bc_subtype: fensapice_flow_bc_subtype_cls = fensapice_flow_bc_subtype_cls
    """
    fensapice_flow_bc_subtype child of pressure_far_field_child.
    """
    fensapice_drop_bccustom: fensapice_drop_bccustom_cls = fensapice_drop_bccustom_cls
    """
    fensapice_drop_bccustom child of pressure_far_field_child.
    """
    fensapice_drop_lwc: fensapice_drop_lwc_cls = fensapice_drop_lwc_cls
    """
    fensapice_drop_lwc child of pressure_far_field_child.
    """
    fensapice_drop_dtemp: fensapice_drop_dtemp_cls = fensapice_drop_dtemp_cls
    """
    fensapice_drop_dtemp child of pressure_far_field_child.
    """
    fensapice_drop_ddiam: fensapice_drop_ddiam_cls = fensapice_drop_ddiam_cls
    """
    fensapice_drop_ddiam child of pressure_far_field_child.
    """
    fensapice_drop_dv: fensapice_drop_dv_cls = fensapice_drop_dv_cls
    """
    fensapice_drop_dv child of pressure_far_field_child.
    """
    fensapice_drop_dx: fensapice_drop_dx_cls = fensapice_drop_dx_cls
    """
    fensapice_drop_dx child of pressure_far_field_child.
    """
    fensapice_drop_dy: fensapice_drop_dy_cls = fensapice_drop_dy_cls
    """
    fensapice_drop_dy child of pressure_far_field_child.
    """
    fensapice_drop_dz: fensapice_drop_dz_cls = fensapice_drop_dz_cls
    """
    fensapice_drop_dz child of pressure_far_field_child.
    """
    fensapice_dpm_surface_injection: fensapice_dpm_surface_injection_cls = fensapice_dpm_surface_injection_cls
    """
    fensapice_dpm_surface_injection child of pressure_far_field_child.
    """
    fensapice_dpm_inj_nstream: fensapice_dpm_inj_nstream_cls = fensapice_dpm_inj_nstream_cls
    """
    fensapice_dpm_inj_nstream child of pressure_far_field_child.
    """
    fensapice_drop_icc: fensapice_drop_icc_cls = fensapice_drop_icc_cls
    """
    fensapice_drop_icc child of pressure_far_field_child.
    """
    fensapice_drop_ctemp: fensapice_drop_ctemp_cls = fensapice_drop_ctemp_cls
    """
    fensapice_drop_ctemp child of pressure_far_field_child.
    """
    fensapice_drop_cdiam: fensapice_drop_cdiam_cls = fensapice_drop_cdiam_cls
    """
    fensapice_drop_cdiam child of pressure_far_field_child.
    """
    fensapice_drop_cv: fensapice_drop_cv_cls = fensapice_drop_cv_cls
    """
    fensapice_drop_cv child of pressure_far_field_child.
    """
    fensapice_drop_cx: fensapice_drop_cx_cls = fensapice_drop_cx_cls
    """
    fensapice_drop_cx child of pressure_far_field_child.
    """
    fensapice_drop_cy: fensapice_drop_cy_cls = fensapice_drop_cy_cls
    """
    fensapice_drop_cy child of pressure_far_field_child.
    """
    fensapice_drop_cz: fensapice_drop_cz_cls = fensapice_drop_cz_cls
    """
    fensapice_drop_cz child of pressure_far_field_child.
    """
    fensapice_drop_vrh: fensapice_drop_vrh_cls = fensapice_drop_vrh_cls
    """
    fensapice_drop_vrh child of pressure_far_field_child.
    """
    fensapice_drop_vrh_1: fensapice_drop_vrh_1_cls = fensapice_drop_vrh_1_cls
    """
    fensapice_drop_vrh_1 child of pressure_far_field_child.
    """
    fensapice_drop_vc: fensapice_drop_vc_cls = fensapice_drop_vc_cls
    """
    fensapice_drop_vc child of pressure_far_field_child.
    """
    uds_bc: uds_bc_cls = uds_bc_cls
    """
    uds_bc child of pressure_far_field_child.
    """
    uds: uds_cls = uds_cls
    """
    uds child of pressure_far_field_child.
    """
    dpm_bc_type: dpm_bc_type_cls = dpm_bc_type_cls
    """
    dpm_bc_type child of pressure_far_field_child.
    """
    dpm_bc_collision_partner: dpm_bc_collision_partner_cls = dpm_bc_collision_partner_cls
    """
    dpm_bc_collision_partner child of pressure_far_field_child.
    """
    reinj_inj: reinj_inj_cls = reinj_inj_cls
    """
    reinj_inj child of pressure_far_field_child.
    """
    dpm_bc_udf: dpm_bc_udf_cls = dpm_bc_udf_cls
    """
    dpm_bc_udf child of pressure_far_field_child.
    """
    solar_fluxes: solar_fluxes_cls = solar_fluxes_cls
    """
    solar_fluxes child of pressure_far_field_child.
    """
    solar_shining_factor: solar_shining_factor_cls = solar_shining_factor_cls
    """
    solar_shining_factor child of pressure_far_field_child.
    """
    radiating_s2s_surface: radiating_s2s_surface_cls = radiating_s2s_surface_cls
    """
    radiating_s2s_surface child of pressure_far_field_child.
    """
