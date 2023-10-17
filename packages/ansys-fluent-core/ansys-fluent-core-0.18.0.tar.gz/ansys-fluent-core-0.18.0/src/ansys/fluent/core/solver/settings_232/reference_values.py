#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .area import area as area_cls
from .depth import depth as depth_cls
from .density_6 import density as density_cls
from .enthalpy import enthalpy as enthalpy_cls
from .length import length as length_cls
from .pressure import pressure as pressure_cls
from .temperature_3 import temperature as temperature_cls
from .yplus import yplus as yplus_cls
from .velocity_2 import velocity as velocity_cls
from .viscosity_3 import viscosity as viscosity_cls
from .zone import zone as zone_cls
from .compute import compute as compute_cls
from .list_val import list_val as list_val_cls
class reference_values(Group):
    """
    'reference_values' child.
    """

    fluent_name = "reference-values"

    child_names = \
        ['area', 'depth', 'density', 'enthalpy', 'length', 'pressure',
         'temperature', 'yplus', 'velocity', 'viscosity', 'zone']

    area: area_cls = area_cls
    """
    area child of reference_values.
    """
    depth: depth_cls = depth_cls
    """
    depth child of reference_values.
    """
    density: density_cls = density_cls
    """
    density child of reference_values.
    """
    enthalpy: enthalpy_cls = enthalpy_cls
    """
    enthalpy child of reference_values.
    """
    length: length_cls = length_cls
    """
    length child of reference_values.
    """
    pressure: pressure_cls = pressure_cls
    """
    pressure child of reference_values.
    """
    temperature: temperature_cls = temperature_cls
    """
    temperature child of reference_values.
    """
    yplus: yplus_cls = yplus_cls
    """
    yplus child of reference_values.
    """
    velocity: velocity_cls = velocity_cls
    """
    velocity child of reference_values.
    """
    viscosity: viscosity_cls = viscosity_cls
    """
    viscosity child of reference_values.
    """
    zone: zone_cls = zone_cls
    """
    zone child of reference_values.
    """
    command_names = \
        ['compute', 'list_val']

    compute: compute_cls = compute_cls
    """
    compute command of reference_values.
    """
    list_val: list_val_cls = list_val_cls
    """
    list_val command of reference_values.
    """
