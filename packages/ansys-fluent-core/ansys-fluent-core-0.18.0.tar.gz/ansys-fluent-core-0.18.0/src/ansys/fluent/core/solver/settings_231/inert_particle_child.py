#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .density_3 import density as density_cls
from .specific_heat_3 import specific_heat as specific_heat_cls
from .thermal_conductivity_3 import thermal_conductivity as thermal_conductivity_cls
from .thermophoretic_co import thermophoretic_co as thermophoretic_co_cls
from .scattering_factor import scattering_factor as scattering_factor_cls
from .emissivity import emissivity as emissivity_cls
from .viscosity_2 import viscosity as viscosity_cls
from .dpm_surften import dpm_surften as dpm_surften_cls
from .electric_conductivity_1 import electric_conductivity as electric_conductivity_cls
from .dual_electric_conductivity_1 import dual_electric_conductivity as dual_electric_conductivity_cls
from .magnetic_permeability import magnetic_permeability as magnetic_permeability_cls
from .charge_density import charge_density as charge_density_cls
class inert_particle_child(Group):
    """
    'child_object_type' of inert_particle.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['density', 'specific_heat', 'thermal_conductivity',
         'thermophoretic_co', 'scattering_factor', 'emissivity', 'viscosity',
         'dpm_surften', 'electric_conductivity', 'dual_electric_conductivity',
         'magnetic_permeability', 'charge_density']

    density: density_cls = density_cls
    """
    density child of inert_particle_child.
    """
    specific_heat: specific_heat_cls = specific_heat_cls
    """
    specific_heat child of inert_particle_child.
    """
    thermal_conductivity: thermal_conductivity_cls = thermal_conductivity_cls
    """
    thermal_conductivity child of inert_particle_child.
    """
    thermophoretic_co: thermophoretic_co_cls = thermophoretic_co_cls
    """
    thermophoretic_co child of inert_particle_child.
    """
    scattering_factor: scattering_factor_cls = scattering_factor_cls
    """
    scattering_factor child of inert_particle_child.
    """
    emissivity: emissivity_cls = emissivity_cls
    """
    emissivity child of inert_particle_child.
    """
    viscosity: viscosity_cls = viscosity_cls
    """
    viscosity child of inert_particle_child.
    """
    dpm_surften: dpm_surften_cls = dpm_surften_cls
    """
    dpm_surften child of inert_particle_child.
    """
    electric_conductivity: electric_conductivity_cls = electric_conductivity_cls
    """
    electric_conductivity child of inert_particle_child.
    """
    dual_electric_conductivity: dual_electric_conductivity_cls = dual_electric_conductivity_cls
    """
    dual_electric_conductivity child of inert_particle_child.
    """
    magnetic_permeability: magnetic_permeability_cls = magnetic_permeability_cls
    """
    magnetic_permeability child of inert_particle_child.
    """
    charge_density: charge_density_cls = charge_density_cls
    """
    charge_density child of inert_particle_child.
    """
