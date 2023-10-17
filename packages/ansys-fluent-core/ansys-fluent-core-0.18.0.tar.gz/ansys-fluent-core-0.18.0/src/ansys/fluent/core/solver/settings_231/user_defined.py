#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .subgrid_scale_turb_visc import subgrid_scale_turb_visc as subgrid_scale_turb_visc_cls
from .turb_visc_func_mf import turb_visc_func_mf as turb_visc_func_mf_cls
from .turb_visc_func import turb_visc_func as turb_visc_func_cls
from .tke_prandtl import tke_prandtl as tke_prandtl_cls
from .tdr_prandtl import tdr_prandtl as tdr_prandtl_cls
from .sdr_prandtl import sdr_prandtl as sdr_prandtl_cls
from .energy_prandtl import energy_prandtl as energy_prandtl_cls
from .wall_prandtl import wall_prandtl as wall_prandtl_cls
from .turbulent_schmidt import turbulent_schmidt as turbulent_schmidt_cls
class user_defined(Group):
    """
    'user_defined' child.
    """

    fluent_name = "user-defined"

    child_names = \
        ['subgrid_scale_turb_visc', 'turb_visc_func_mf', 'turb_visc_func',
         'tke_prandtl', 'tdr_prandtl', 'sdr_prandtl', 'energy_prandtl',
         'wall_prandtl', 'turbulent_schmidt']

    subgrid_scale_turb_visc: subgrid_scale_turb_visc_cls = subgrid_scale_turb_visc_cls
    """
    subgrid_scale_turb_visc child of user_defined.
    """
    turb_visc_func_mf: turb_visc_func_mf_cls = turb_visc_func_mf_cls
    """
    turb_visc_func_mf child of user_defined.
    """
    turb_visc_func: turb_visc_func_cls = turb_visc_func_cls
    """
    turb_visc_func child of user_defined.
    """
    tke_prandtl: tke_prandtl_cls = tke_prandtl_cls
    """
    tke_prandtl child of user_defined.
    """
    tdr_prandtl: tdr_prandtl_cls = tdr_prandtl_cls
    """
    tdr_prandtl child of user_defined.
    """
    sdr_prandtl: sdr_prandtl_cls = sdr_prandtl_cls
    """
    sdr_prandtl child of user_defined.
    """
    energy_prandtl: energy_prandtl_cls = energy_prandtl_cls
    """
    energy_prandtl child of user_defined.
    """
    wall_prandtl: wall_prandtl_cls = wall_prandtl_cls
    """
    wall_prandtl child of user_defined.
    """
    turbulent_schmidt: turbulent_schmidt_cls = turbulent_schmidt_cls
    """
    turbulent_schmidt child of user_defined.
    """
