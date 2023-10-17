#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .phase_4 import phase as phase_cls
from .geom_disable import geom_disable as geom_disable_cls
from .geom_dir_spec import geom_dir_spec as geom_dir_spec_cls
from .geom_dir_x import geom_dir_x as geom_dir_x_cls
from .geom_dir_y import geom_dir_y as geom_dir_y_cls
from .geom_dir_z import geom_dir_z as geom_dir_z_cls
from .geom_levels import geom_levels as geom_levels_cls
from .geom_bgthread import geom_bgthread as geom_bgthread_cls
from .porous_jump_turb_wall_treatment import porous_jump_turb_wall_treatment as porous_jump_turb_wall_treatment_cls
from .dir import dir as dir_cls
from .average_dp import average_dp as average_dp_cls
from .c import c as c_cls
from .limit_range import limit_range as limit_range_cls
from .v_min import v_min as v_min_cls
from .v_max import v_max as v_max_cls
from .strength import strength as strength_cls
from .profile_dp import profile_dp as profile_dp_cls
from .dp_profile import dp_profile as dp_profile_cls
from .swirl_model import swirl_model as swirl_model_cls
from .fan_vr import fan_vr as fan_vr_cls
from .fr import fr as fr_cls
from .hub import hub as hub_cls
from .axis_origin_component_1 import axis_origin_component as axis_origin_component_cls
from .axis_direction_component_1 import axis_direction_component as axis_direction_component_cls
from .profile_vt import profile_vt as profile_vt_cls
from .vt_profile import vt_profile as vt_profile_cls
from .profile_vr import profile_vr as profile_vr_cls
from .vr_profile import vr_profile as vr_profile_cls
from .swirl_factor import swirl_factor as swirl_factor_cls
from .dpm_bc_type import dpm_bc_type as dpm_bc_type_cls
from .dpm_bc_collision_partner import dpm_bc_collision_partner as dpm_bc_collision_partner_cls
from .reinj_inj import reinj_inj as reinj_inj_cls
from .dpm_bc_udf import dpm_bc_udf as dpm_bc_udf_cls
from .new_fan_definition import new_fan_definition as new_fan_definition_cls
class fan_child(Group):
    """
    'child_object_type' of fan.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['phase', 'geom_disable', 'geom_dir_spec', 'geom_dir_x', 'geom_dir_y',
         'geom_dir_z', 'geom_levels', 'geom_bgthread',
         'porous_jump_turb_wall_treatment', 'dir', 'average_dp', 'c',
         'limit_range', 'v_min', 'v_max', 'strength', 'profile_dp',
         'dp_profile', 'swirl_model', 'fan_vr', 'fr', 'hub',
         'axis_origin_component', 'axis_direction_component', 'profile_vt',
         'vt_profile', 'profile_vr', 'vr_profile', 'swirl_factor',
         'dpm_bc_type', 'dpm_bc_collision_partner', 'reinj_inj', 'dpm_bc_udf',
         'new_fan_definition']

    phase: phase_cls = phase_cls
    """
    phase child of fan_child.
    """
    geom_disable: geom_disable_cls = geom_disable_cls
    """
    geom_disable child of fan_child.
    """
    geom_dir_spec: geom_dir_spec_cls = geom_dir_spec_cls
    """
    geom_dir_spec child of fan_child.
    """
    geom_dir_x: geom_dir_x_cls = geom_dir_x_cls
    """
    geom_dir_x child of fan_child.
    """
    geom_dir_y: geom_dir_y_cls = geom_dir_y_cls
    """
    geom_dir_y child of fan_child.
    """
    geom_dir_z: geom_dir_z_cls = geom_dir_z_cls
    """
    geom_dir_z child of fan_child.
    """
    geom_levels: geom_levels_cls = geom_levels_cls
    """
    geom_levels child of fan_child.
    """
    geom_bgthread: geom_bgthread_cls = geom_bgthread_cls
    """
    geom_bgthread child of fan_child.
    """
    porous_jump_turb_wall_treatment: porous_jump_turb_wall_treatment_cls = porous_jump_turb_wall_treatment_cls
    """
    porous_jump_turb_wall_treatment child of fan_child.
    """
    dir: dir_cls = dir_cls
    """
    dir child of fan_child.
    """
    average_dp: average_dp_cls = average_dp_cls
    """
    average_dp child of fan_child.
    """
    c: c_cls = c_cls
    """
    c child of fan_child.
    """
    limit_range: limit_range_cls = limit_range_cls
    """
    limit_range child of fan_child.
    """
    v_min: v_min_cls = v_min_cls
    """
    v_min child of fan_child.
    """
    v_max: v_max_cls = v_max_cls
    """
    v_max child of fan_child.
    """
    strength: strength_cls = strength_cls
    """
    strength child of fan_child.
    """
    profile_dp: profile_dp_cls = profile_dp_cls
    """
    profile_dp child of fan_child.
    """
    dp_profile: dp_profile_cls = dp_profile_cls
    """
    dp_profile child of fan_child.
    """
    swirl_model: swirl_model_cls = swirl_model_cls
    """
    swirl_model child of fan_child.
    """
    fan_vr: fan_vr_cls = fan_vr_cls
    """
    fan_vr child of fan_child.
    """
    fr: fr_cls = fr_cls
    """
    fr child of fan_child.
    """
    hub: hub_cls = hub_cls
    """
    hub child of fan_child.
    """
    axis_origin_component: axis_origin_component_cls = axis_origin_component_cls
    """
    axis_origin_component child of fan_child.
    """
    axis_direction_component: axis_direction_component_cls = axis_direction_component_cls
    """
    axis_direction_component child of fan_child.
    """
    profile_vt: profile_vt_cls = profile_vt_cls
    """
    profile_vt child of fan_child.
    """
    vt_profile: vt_profile_cls = vt_profile_cls
    """
    vt_profile child of fan_child.
    """
    profile_vr: profile_vr_cls = profile_vr_cls
    """
    profile_vr child of fan_child.
    """
    vr_profile: vr_profile_cls = vr_profile_cls
    """
    vr_profile child of fan_child.
    """
    swirl_factor: swirl_factor_cls = swirl_factor_cls
    """
    swirl_factor child of fan_child.
    """
    dpm_bc_type: dpm_bc_type_cls = dpm_bc_type_cls
    """
    dpm_bc_type child of fan_child.
    """
    dpm_bc_collision_partner: dpm_bc_collision_partner_cls = dpm_bc_collision_partner_cls
    """
    dpm_bc_collision_partner child of fan_child.
    """
    reinj_inj: reinj_inj_cls = reinj_inj_cls
    """
    reinj_inj child of fan_child.
    """
    dpm_bc_udf: dpm_bc_udf_cls = dpm_bc_udf_cls
    """
    dpm_bc_udf child of fan_child.
    """
    new_fan_definition: new_fan_definition_cls = new_fan_definition_cls
    """
    new_fan_definition child of fan_child.
    """
