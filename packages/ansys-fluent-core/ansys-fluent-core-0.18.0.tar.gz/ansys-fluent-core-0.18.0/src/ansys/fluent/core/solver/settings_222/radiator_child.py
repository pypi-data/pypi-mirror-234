#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .phase_19 import phase as phase_cls
from .geom_disable import geom_disable as geom_disable_cls
from .geom_dir_spec import geom_dir_spec as geom_dir_spec_cls
from .geom_dir_x import geom_dir_x as geom_dir_x_cls
from .geom_dir_y import geom_dir_y as geom_dir_y_cls
from .geom_dir_z import geom_dir_z as geom_dir_z_cls
from .geom_levels import geom_levels as geom_levels_cls
from .geom_bgthread import geom_bgthread as geom_bgthread_cls
from .porous_jump_turb_wall_treatment import porous_jump_turb_wall_treatment as porous_jump_turb_wall_treatment_cls
from .kc import kc as kc_cls
from .hc import hc as hc_cls
from .t_1 import t as t_cls
from .q_1 import q as q_cls
from .dpm_bc_type import dpm_bc_type as dpm_bc_type_cls
from .dpm_bc_collision_partner import dpm_bc_collision_partner as dpm_bc_collision_partner_cls
from .reinj_inj import reinj_inj as reinj_inj_cls
from .dpm_bc_udf import dpm_bc_udf as dpm_bc_udf_cls
from .strength import strength as strength_cls
class radiator_child(Group):
    """
    'child_object_type' of radiator.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['phase', 'geom_disable', 'geom_dir_spec', 'geom_dir_x', 'geom_dir_y',
         'geom_dir_z', 'geom_levels', 'geom_bgthread',
         'porous_jump_turb_wall_treatment', 'kc', 'hc', 't', 'q',
         'dpm_bc_type', 'dpm_bc_collision_partner', 'reinj_inj', 'dpm_bc_udf',
         'strength']

    phase: phase_cls = phase_cls
    """
    phase child of radiator_child.
    """
    geom_disable: geom_disable_cls = geom_disable_cls
    """
    geom_disable child of radiator_child.
    """
    geom_dir_spec: geom_dir_spec_cls = geom_dir_spec_cls
    """
    geom_dir_spec child of radiator_child.
    """
    geom_dir_x: geom_dir_x_cls = geom_dir_x_cls
    """
    geom_dir_x child of radiator_child.
    """
    geom_dir_y: geom_dir_y_cls = geom_dir_y_cls
    """
    geom_dir_y child of radiator_child.
    """
    geom_dir_z: geom_dir_z_cls = geom_dir_z_cls
    """
    geom_dir_z child of radiator_child.
    """
    geom_levels: geom_levels_cls = geom_levels_cls
    """
    geom_levels child of radiator_child.
    """
    geom_bgthread: geom_bgthread_cls = geom_bgthread_cls
    """
    geom_bgthread child of radiator_child.
    """
    porous_jump_turb_wall_treatment: porous_jump_turb_wall_treatment_cls = porous_jump_turb_wall_treatment_cls
    """
    porous_jump_turb_wall_treatment child of radiator_child.
    """
    kc: kc_cls = kc_cls
    """
    kc child of radiator_child.
    """
    hc: hc_cls = hc_cls
    """
    hc child of radiator_child.
    """
    t: t_cls = t_cls
    """
    t child of radiator_child.
    """
    q: q_cls = q_cls
    """
    q child of radiator_child.
    """
    dpm_bc_type: dpm_bc_type_cls = dpm_bc_type_cls
    """
    dpm_bc_type child of radiator_child.
    """
    dpm_bc_collision_partner: dpm_bc_collision_partner_cls = dpm_bc_collision_partner_cls
    """
    dpm_bc_collision_partner child of radiator_child.
    """
    reinj_inj: reinj_inj_cls = reinj_inj_cls
    """
    reinj_inj child of radiator_child.
    """
    dpm_bc_udf: dpm_bc_udf_cls = dpm_bc_udf_cls
    """
    dpm_bc_udf child of radiator_child.
    """
    strength: strength_cls = strength_cls
    """
    strength child of radiator_child.
    """
