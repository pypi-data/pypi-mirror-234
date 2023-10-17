#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .geom_disable import geom_disable as geom_disable_cls
from .geom_dir_spec import geom_dir_spec as geom_dir_spec_cls
from .geom_dir_x import geom_dir_x as geom_dir_x_cls
from .geom_dir_y import geom_dir_y as geom_dir_y_cls
from .geom_dir_z import geom_dir_z as geom_dir_z_cls
from .geom_levels import geom_levels as geom_levels_cls
from .geom_bgthread import geom_bgthread as geom_bgthread_cls
from .flowrate_frac import flowrate_frac as flowrate_frac_cls
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
from .uds_bc import uds_bc as uds_bc_cls
from .uds import uds as uds_cls
from .radiation_bc import radiation_bc as radiation_bc_cls
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
from .dpm_bc_type import dpm_bc_type as dpm_bc_type_cls
from .dpm_bc_collision_partner import dpm_bc_collision_partner as dpm_bc_collision_partner_cls
from .reinj_inj import reinj_inj as reinj_inj_cls
from .dpm_bc_udf import dpm_bc_udf as dpm_bc_udf_cls
from .solar_fluxes import solar_fluxes as solar_fluxes_cls
from .solar_shining_factor import solar_shining_factor as solar_shining_factor_cls
from .radiating_s2s_surface import radiating_s2s_surface as radiating_s2s_surface_cls
class phase_child(Group):
    """
    'child_object_type' of phase.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['geom_disable', 'geom_dir_spec', 'geom_dir_x', 'geom_dir_y',
         'geom_dir_z', 'geom_levels', 'geom_bgthread', 'flowrate_frac',
         'elec_potential_type', 'potential_value', 'dual_potential_type',
         'dual_potential_value', 'x_displacement_type',
         'x_displacement_value', 'y_displacement_type',
         'y_displacement_value', 'z_displacement_type',
         'z_displacement_value', 'uds_bc', 'uds', 'radiation_bc',
         'coll_dtheta', 'coll_dphi', 'band_q_irrad', 'band_q_irrad_diffuse',
         'parallel_collimated_beam', 'solar_direction', 'solar_irradiation',
         't_b_b_spec', 't_b_b', 'in_emiss', 'dpm_bc_type',
         'dpm_bc_collision_partner', 'reinj_inj', 'dpm_bc_udf',
         'solar_fluxes', 'solar_shining_factor', 'radiating_s2s_surface']

    geom_disable: geom_disable_cls = geom_disable_cls
    """
    geom_disable child of phase_child.
    """
    geom_dir_spec: geom_dir_spec_cls = geom_dir_spec_cls
    """
    geom_dir_spec child of phase_child.
    """
    geom_dir_x: geom_dir_x_cls = geom_dir_x_cls
    """
    geom_dir_x child of phase_child.
    """
    geom_dir_y: geom_dir_y_cls = geom_dir_y_cls
    """
    geom_dir_y child of phase_child.
    """
    geom_dir_z: geom_dir_z_cls = geom_dir_z_cls
    """
    geom_dir_z child of phase_child.
    """
    geom_levels: geom_levels_cls = geom_levels_cls
    """
    geom_levels child of phase_child.
    """
    geom_bgthread: geom_bgthread_cls = geom_bgthread_cls
    """
    geom_bgthread child of phase_child.
    """
    flowrate_frac: flowrate_frac_cls = flowrate_frac_cls
    """
    flowrate_frac child of phase_child.
    """
    elec_potential_type: elec_potential_type_cls = elec_potential_type_cls
    """
    elec_potential_type child of phase_child.
    """
    potential_value: potential_value_cls = potential_value_cls
    """
    potential_value child of phase_child.
    """
    dual_potential_type: dual_potential_type_cls = dual_potential_type_cls
    """
    dual_potential_type child of phase_child.
    """
    dual_potential_value: dual_potential_value_cls = dual_potential_value_cls
    """
    dual_potential_value child of phase_child.
    """
    x_displacement_type: x_displacement_type_cls = x_displacement_type_cls
    """
    x_displacement_type child of phase_child.
    """
    x_displacement_value: x_displacement_value_cls = x_displacement_value_cls
    """
    x_displacement_value child of phase_child.
    """
    y_displacement_type: y_displacement_type_cls = y_displacement_type_cls
    """
    y_displacement_type child of phase_child.
    """
    y_displacement_value: y_displacement_value_cls = y_displacement_value_cls
    """
    y_displacement_value child of phase_child.
    """
    z_displacement_type: z_displacement_type_cls = z_displacement_type_cls
    """
    z_displacement_type child of phase_child.
    """
    z_displacement_value: z_displacement_value_cls = z_displacement_value_cls
    """
    z_displacement_value child of phase_child.
    """
    uds_bc: uds_bc_cls = uds_bc_cls
    """
    uds_bc child of phase_child.
    """
    uds: uds_cls = uds_cls
    """
    uds child of phase_child.
    """
    radiation_bc: radiation_bc_cls = radiation_bc_cls
    """
    radiation_bc child of phase_child.
    """
    coll_dtheta: coll_dtheta_cls = coll_dtheta_cls
    """
    coll_dtheta child of phase_child.
    """
    coll_dphi: coll_dphi_cls = coll_dphi_cls
    """
    coll_dphi child of phase_child.
    """
    band_q_irrad: band_q_irrad_cls = band_q_irrad_cls
    """
    band_q_irrad child of phase_child.
    """
    band_q_irrad_diffuse: band_q_irrad_diffuse_cls = band_q_irrad_diffuse_cls
    """
    band_q_irrad_diffuse child of phase_child.
    """
    parallel_collimated_beam: parallel_collimated_beam_cls = parallel_collimated_beam_cls
    """
    parallel_collimated_beam child of phase_child.
    """
    solar_direction: solar_direction_cls = solar_direction_cls
    """
    solar_direction child of phase_child.
    """
    solar_irradiation: solar_irradiation_cls = solar_irradiation_cls
    """
    solar_irradiation child of phase_child.
    """
    t_b_b_spec: t_b_b_spec_cls = t_b_b_spec_cls
    """
    t_b_b_spec child of phase_child.
    """
    t_b_b: t_b_b_cls = t_b_b_cls
    """
    t_b_b child of phase_child.
    """
    in_emiss: in_emiss_cls = in_emiss_cls
    """
    in_emiss child of phase_child.
    """
    dpm_bc_type: dpm_bc_type_cls = dpm_bc_type_cls
    """
    dpm_bc_type child of phase_child.
    """
    dpm_bc_collision_partner: dpm_bc_collision_partner_cls = dpm_bc_collision_partner_cls
    """
    dpm_bc_collision_partner child of phase_child.
    """
    reinj_inj: reinj_inj_cls = reinj_inj_cls
    """
    reinj_inj child of phase_child.
    """
    dpm_bc_udf: dpm_bc_udf_cls = dpm_bc_udf_cls
    """
    dpm_bc_udf child of phase_child.
    """
    solar_fluxes: solar_fluxes_cls = solar_fluxes_cls
    """
    solar_fluxes child of phase_child.
    """
    solar_shining_factor: solar_shining_factor_cls = solar_shining_factor_cls
    """
    solar_shining_factor child of phase_child.
    """
    radiating_s2s_surface: radiating_s2s_surface_cls = radiating_s2s_surface_cls
    """
    radiating_s2s_surface child of phase_child.
    """
