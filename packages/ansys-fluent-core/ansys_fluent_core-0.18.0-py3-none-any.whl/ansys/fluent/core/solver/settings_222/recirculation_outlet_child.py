#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .phase_22 import phase as phase_cls
from .geom_disable import geom_disable as geom_disable_cls
from .geom_dir_spec import geom_dir_spec as geom_dir_spec_cls
from .geom_dir_x import geom_dir_x as geom_dir_x_cls
from .geom_dir_y import geom_dir_y as geom_dir_y_cls
from .geom_dir_z import geom_dir_z as geom_dir_z_cls
from .geom_levels import geom_levels as geom_levels_cls
from .geom_bgthread import geom_bgthread as geom_bgthread_cls
from .flow_spec import flow_spec as flow_spec_cls
from .mass_flow import mass_flow as mass_flow_cls
from .mass_flux import mass_flux as mass_flux_cls
from .solar_fluxes import solar_fluxes as solar_fluxes_cls
from .solar_shining_factor import solar_shining_factor as solar_shining_factor_cls
class recirculation_outlet_child(Group):
    """
    'child_object_type' of recirculation_outlet.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['phase', 'geom_disable', 'geom_dir_spec', 'geom_dir_x', 'geom_dir_y',
         'geom_dir_z', 'geom_levels', 'geom_bgthread', 'flow_spec',
         'mass_flow', 'mass_flux', 'solar_fluxes', 'solar_shining_factor']

    phase: phase_cls = phase_cls
    """
    phase child of recirculation_outlet_child.
    """
    geom_disable: geom_disable_cls = geom_disable_cls
    """
    geom_disable child of recirculation_outlet_child.
    """
    geom_dir_spec: geom_dir_spec_cls = geom_dir_spec_cls
    """
    geom_dir_spec child of recirculation_outlet_child.
    """
    geom_dir_x: geom_dir_x_cls = geom_dir_x_cls
    """
    geom_dir_x child of recirculation_outlet_child.
    """
    geom_dir_y: geom_dir_y_cls = geom_dir_y_cls
    """
    geom_dir_y child of recirculation_outlet_child.
    """
    geom_dir_z: geom_dir_z_cls = geom_dir_z_cls
    """
    geom_dir_z child of recirculation_outlet_child.
    """
    geom_levels: geom_levels_cls = geom_levels_cls
    """
    geom_levels child of recirculation_outlet_child.
    """
    geom_bgthread: geom_bgthread_cls = geom_bgthread_cls
    """
    geom_bgthread child of recirculation_outlet_child.
    """
    flow_spec: flow_spec_cls = flow_spec_cls
    """
    flow_spec child of recirculation_outlet_child.
    """
    mass_flow: mass_flow_cls = mass_flow_cls
    """
    mass_flow child of recirculation_outlet_child.
    """
    mass_flux: mass_flux_cls = mass_flux_cls
    """
    mass_flux child of recirculation_outlet_child.
    """
    solar_fluxes: solar_fluxes_cls = solar_fluxes_cls
    """
    solar_fluxes child of recirculation_outlet_child.
    """
    solar_shining_factor: solar_shining_factor_cls = solar_shining_factor_cls
    """
    solar_shining_factor child of recirculation_outlet_child.
    """
