#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .phase_15 import phase as phase_cls
from .geom_disable import geom_disable as geom_disable_cls
from .geom_dir_spec import geom_dir_spec as geom_dir_spec_cls
from .geom_dir_x import geom_dir_x as geom_dir_x_cls
from .geom_dir_y import geom_dir_y as geom_dir_y_cls
from .geom_dir_z import geom_dir_z as geom_dir_z_cls
from .geom_levels import geom_levels as geom_levels_cls
from .geom_bgthread import geom_bgthread as geom_bgthread_cls
from .porous_jump_turb_wall_treatment import porous_jump_turb_wall_treatment as porous_jump_turb_wall_treatment_cls
from .alpha import alpha as alpha_cls
from .dm import dm as dm_cls
from .c2 import c2 as c2_cls
from .thermal_ctk import thermal_ctk as thermal_ctk_cls
from .solar_fluxes import solar_fluxes as solar_fluxes_cls
from .v_absp import v_absp as v_absp_cls
from .ir_absp import ir_absp as ir_absp_cls
from .ir_trans import ir_trans as ir_trans_cls
from .v_trans import v_trans as v_trans_cls
from .dpm_bc_type import dpm_bc_type as dpm_bc_type_cls
from .dpm_bc_collision_partner import dpm_bc_collision_partner as dpm_bc_collision_partner_cls
from .reinj_inj import reinj_inj as reinj_inj_cls
from .dpm_bc_udf import dpm_bc_udf as dpm_bc_udf_cls
from .strength import strength as strength_cls
from .jump_adhesion import jump_adhesion as jump_adhesion_cls
from .adhesion_constrained import adhesion_constrained as adhesion_constrained_cls
from .adhesion_angle import adhesion_angle as adhesion_angle_cls
from .x_displacement_type import x_displacement_type as x_displacement_type_cls
from .x_displacement_value import x_displacement_value as x_displacement_value_cls
from .y_displacement_type import y_displacement_type as y_displacement_type_cls
from .y_displacement_value import y_displacement_value as y_displacement_value_cls
from .z_displacement_type import z_displacement_type as z_displacement_type_cls
from .z_displacement_value import z_displacement_value as z_displacement_value_cls
class porous_jump_child(Group):
    """
    'child_object_type' of porous_jump.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['phase', 'geom_disable', 'geom_dir_spec', 'geom_dir_x', 'geom_dir_y',
         'geom_dir_z', 'geom_levels', 'geom_bgthread',
         'porous_jump_turb_wall_treatment', 'alpha', 'dm', 'c2',
         'thermal_ctk', 'solar_fluxes', 'v_absp', 'ir_absp', 'ir_trans',
         'v_trans', 'dpm_bc_type', 'dpm_bc_collision_partner', 'reinj_inj',
         'dpm_bc_udf', 'strength', 'jump_adhesion', 'adhesion_constrained',
         'adhesion_angle', 'x_displacement_type', 'x_displacement_value',
         'y_displacement_type', 'y_displacement_value', 'z_displacement_type',
         'z_displacement_value']

    phase: phase_cls = phase_cls
    """
    phase child of porous_jump_child.
    """
    geom_disable: geom_disable_cls = geom_disable_cls
    """
    geom_disable child of porous_jump_child.
    """
    geom_dir_spec: geom_dir_spec_cls = geom_dir_spec_cls
    """
    geom_dir_spec child of porous_jump_child.
    """
    geom_dir_x: geom_dir_x_cls = geom_dir_x_cls
    """
    geom_dir_x child of porous_jump_child.
    """
    geom_dir_y: geom_dir_y_cls = geom_dir_y_cls
    """
    geom_dir_y child of porous_jump_child.
    """
    geom_dir_z: geom_dir_z_cls = geom_dir_z_cls
    """
    geom_dir_z child of porous_jump_child.
    """
    geom_levels: geom_levels_cls = geom_levels_cls
    """
    geom_levels child of porous_jump_child.
    """
    geom_bgthread: geom_bgthread_cls = geom_bgthread_cls
    """
    geom_bgthread child of porous_jump_child.
    """
    porous_jump_turb_wall_treatment: porous_jump_turb_wall_treatment_cls = porous_jump_turb_wall_treatment_cls
    """
    porous_jump_turb_wall_treatment child of porous_jump_child.
    """
    alpha: alpha_cls = alpha_cls
    """
    alpha child of porous_jump_child.
    """
    dm: dm_cls = dm_cls
    """
    dm child of porous_jump_child.
    """
    c2: c2_cls = c2_cls
    """
    c2 child of porous_jump_child.
    """
    thermal_ctk: thermal_ctk_cls = thermal_ctk_cls
    """
    thermal_ctk child of porous_jump_child.
    """
    solar_fluxes: solar_fluxes_cls = solar_fluxes_cls
    """
    solar_fluxes child of porous_jump_child.
    """
    v_absp: v_absp_cls = v_absp_cls
    """
    v_absp child of porous_jump_child.
    """
    ir_absp: ir_absp_cls = ir_absp_cls
    """
    ir_absp child of porous_jump_child.
    """
    ir_trans: ir_trans_cls = ir_trans_cls
    """
    ir_trans child of porous_jump_child.
    """
    v_trans: v_trans_cls = v_trans_cls
    """
    v_trans child of porous_jump_child.
    """
    dpm_bc_type: dpm_bc_type_cls = dpm_bc_type_cls
    """
    dpm_bc_type child of porous_jump_child.
    """
    dpm_bc_collision_partner: dpm_bc_collision_partner_cls = dpm_bc_collision_partner_cls
    """
    dpm_bc_collision_partner child of porous_jump_child.
    """
    reinj_inj: reinj_inj_cls = reinj_inj_cls
    """
    reinj_inj child of porous_jump_child.
    """
    dpm_bc_udf: dpm_bc_udf_cls = dpm_bc_udf_cls
    """
    dpm_bc_udf child of porous_jump_child.
    """
    strength: strength_cls = strength_cls
    """
    strength child of porous_jump_child.
    """
    jump_adhesion: jump_adhesion_cls = jump_adhesion_cls
    """
    jump_adhesion child of porous_jump_child.
    """
    adhesion_constrained: adhesion_constrained_cls = adhesion_constrained_cls
    """
    adhesion_constrained child of porous_jump_child.
    """
    adhesion_angle: adhesion_angle_cls = adhesion_angle_cls
    """
    adhesion_angle child of porous_jump_child.
    """
    x_displacement_type: x_displacement_type_cls = x_displacement_type_cls
    """
    x_displacement_type child of porous_jump_child.
    """
    x_displacement_value: x_displacement_value_cls = x_displacement_value_cls
    """
    x_displacement_value child of porous_jump_child.
    """
    y_displacement_type: y_displacement_type_cls = y_displacement_type_cls
    """
    y_displacement_type child of porous_jump_child.
    """
    y_displacement_value: y_displacement_value_cls = y_displacement_value_cls
    """
    y_displacement_value child of porous_jump_child.
    """
    z_displacement_type: z_displacement_type_cls = z_displacement_type_cls
    """
    z_displacement_type child of porous_jump_child.
    """
    z_displacement_value: z_displacement_value_cls = z_displacement_value_cls
    """
    z_displacement_value child of porous_jump_child.
    """
