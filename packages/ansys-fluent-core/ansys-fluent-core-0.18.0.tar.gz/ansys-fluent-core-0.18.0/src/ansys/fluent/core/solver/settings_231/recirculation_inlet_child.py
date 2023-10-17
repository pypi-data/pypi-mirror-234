#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .phase_21 import phase as phase_cls
from .geom_disable import geom_disable as geom_disable_cls
from .geom_dir_spec import geom_dir_spec as geom_dir_spec_cls
from .geom_dir_x import geom_dir_x as geom_dir_x_cls
from .geom_dir_y import geom_dir_y as geom_dir_y_cls
from .geom_dir_z import geom_dir_z as geom_dir_z_cls
from .geom_levels import geom_levels as geom_levels_cls
from .geom_bgthread import geom_bgthread as geom_bgthread_cls
from .pid import pid as pid_cls
from .temperature_spec import temperature_spec as temperature_spec_cls
from .temperature_rise import temperature_rise as temperature_rise_cls
from .heat_source import heat_source as heat_source_cls
from .tinf import tinf as tinf_cls
from .hc import hc as hc_cls
from .direction_spec import direction_spec as direction_spec_cls
from .coordinate_system import coordinate_system as coordinate_system_cls
from .flow_direction import flow_direction as flow_direction_cls
from .direction_vector import direction_vector as direction_vector_cls
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
from .mass_flow_multiplier import mass_flow_multiplier as mass_flow_multiplier_cls
from .solar_fluxes import solar_fluxes as solar_fluxes_cls
from .solar_shining_factor import solar_shining_factor as solar_shining_factor_cls
class recirculation_inlet_child(Group):
    """
    'child_object_type' of recirculation_inlet.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['phase', 'geom_disable', 'geom_dir_spec', 'geom_dir_x', 'geom_dir_y',
         'geom_dir_z', 'geom_levels', 'geom_bgthread', 'pid',
         'temperature_spec', 'temperature_rise', 'heat_source', 'tinf', 'hc',
         'direction_spec', 'coordinate_system', 'flow_direction',
         'direction_vector', 'ke_spec', 'nut', 'kl', 'intermit', 'k', 'e',
         'o', 'v2', 'turb_intensity', 'turb_length_scale',
         'turb_hydraulic_diam', 'turb_viscosity_ratio',
         'turb_viscosity_ratio_profile', 'rst_spec', 'uu', 'vv', 'ww', 'uv',
         'vw', 'uw', 'ksgs_spec', 'ksgs', 'sgs_turb_intensity',
         'mass_flow_multiplier', 'solar_fluxes', 'solar_shining_factor']

    phase: phase_cls = phase_cls
    """
    phase child of recirculation_inlet_child.
    """
    geom_disable: geom_disable_cls = geom_disable_cls
    """
    geom_disable child of recirculation_inlet_child.
    """
    geom_dir_spec: geom_dir_spec_cls = geom_dir_spec_cls
    """
    geom_dir_spec child of recirculation_inlet_child.
    """
    geom_dir_x: geom_dir_x_cls = geom_dir_x_cls
    """
    geom_dir_x child of recirculation_inlet_child.
    """
    geom_dir_y: geom_dir_y_cls = geom_dir_y_cls
    """
    geom_dir_y child of recirculation_inlet_child.
    """
    geom_dir_z: geom_dir_z_cls = geom_dir_z_cls
    """
    geom_dir_z child of recirculation_inlet_child.
    """
    geom_levels: geom_levels_cls = geom_levels_cls
    """
    geom_levels child of recirculation_inlet_child.
    """
    geom_bgthread: geom_bgthread_cls = geom_bgthread_cls
    """
    geom_bgthread child of recirculation_inlet_child.
    """
    pid: pid_cls = pid_cls
    """
    pid child of recirculation_inlet_child.
    """
    temperature_spec: temperature_spec_cls = temperature_spec_cls
    """
    temperature_spec child of recirculation_inlet_child.
    """
    temperature_rise: temperature_rise_cls = temperature_rise_cls
    """
    temperature_rise child of recirculation_inlet_child.
    """
    heat_source: heat_source_cls = heat_source_cls
    """
    heat_source child of recirculation_inlet_child.
    """
    tinf: tinf_cls = tinf_cls
    """
    tinf child of recirculation_inlet_child.
    """
    hc: hc_cls = hc_cls
    """
    hc child of recirculation_inlet_child.
    """
    direction_spec: direction_spec_cls = direction_spec_cls
    """
    direction_spec child of recirculation_inlet_child.
    """
    coordinate_system: coordinate_system_cls = coordinate_system_cls
    """
    coordinate_system child of recirculation_inlet_child.
    """
    flow_direction: flow_direction_cls = flow_direction_cls
    """
    flow_direction child of recirculation_inlet_child.
    """
    direction_vector: direction_vector_cls = direction_vector_cls
    """
    direction_vector child of recirculation_inlet_child.
    """
    ke_spec: ke_spec_cls = ke_spec_cls
    """
    ke_spec child of recirculation_inlet_child.
    """
    nut: nut_cls = nut_cls
    """
    nut child of recirculation_inlet_child.
    """
    kl: kl_cls = kl_cls
    """
    kl child of recirculation_inlet_child.
    """
    intermit: intermit_cls = intermit_cls
    """
    intermit child of recirculation_inlet_child.
    """
    k: k_cls = k_cls
    """
    k child of recirculation_inlet_child.
    """
    e: e_cls = e_cls
    """
    e child of recirculation_inlet_child.
    """
    o: o_cls = o_cls
    """
    o child of recirculation_inlet_child.
    """
    v2: v2_cls = v2_cls
    """
    v2 child of recirculation_inlet_child.
    """
    turb_intensity: turb_intensity_cls = turb_intensity_cls
    """
    turb_intensity child of recirculation_inlet_child.
    """
    turb_length_scale: turb_length_scale_cls = turb_length_scale_cls
    """
    turb_length_scale child of recirculation_inlet_child.
    """
    turb_hydraulic_diam: turb_hydraulic_diam_cls = turb_hydraulic_diam_cls
    """
    turb_hydraulic_diam child of recirculation_inlet_child.
    """
    turb_viscosity_ratio: turb_viscosity_ratio_cls = turb_viscosity_ratio_cls
    """
    turb_viscosity_ratio child of recirculation_inlet_child.
    """
    turb_viscosity_ratio_profile: turb_viscosity_ratio_profile_cls = turb_viscosity_ratio_profile_cls
    """
    turb_viscosity_ratio_profile child of recirculation_inlet_child.
    """
    rst_spec: rst_spec_cls = rst_spec_cls
    """
    rst_spec child of recirculation_inlet_child.
    """
    uu: uu_cls = uu_cls
    """
    uu child of recirculation_inlet_child.
    """
    vv: vv_cls = vv_cls
    """
    vv child of recirculation_inlet_child.
    """
    ww: ww_cls = ww_cls
    """
    ww child of recirculation_inlet_child.
    """
    uv: uv_cls = uv_cls
    """
    uv child of recirculation_inlet_child.
    """
    vw: vw_cls = vw_cls
    """
    vw child of recirculation_inlet_child.
    """
    uw: uw_cls = uw_cls
    """
    uw child of recirculation_inlet_child.
    """
    ksgs_spec: ksgs_spec_cls = ksgs_spec_cls
    """
    ksgs_spec child of recirculation_inlet_child.
    """
    ksgs: ksgs_cls = ksgs_cls
    """
    ksgs child of recirculation_inlet_child.
    """
    sgs_turb_intensity: sgs_turb_intensity_cls = sgs_turb_intensity_cls
    """
    sgs_turb_intensity child of recirculation_inlet_child.
    """
    mass_flow_multiplier: mass_flow_multiplier_cls = mass_flow_multiplier_cls
    """
    mass_flow_multiplier child of recirculation_inlet_child.
    """
    solar_fluxes: solar_fluxes_cls = solar_fluxes_cls
    """
    solar_fluxes child of recirculation_inlet_child.
    """
    solar_shining_factor: solar_shining_factor_cls = solar_shining_factor_cls
    """
    solar_shining_factor child of recirculation_inlet_child.
    """
