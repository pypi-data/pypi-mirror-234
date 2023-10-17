#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .name_1 import name as name_cls
from .chemical_formula import chemical_formula as chemical_formula_cls
from .density import density as density_cls
from .viscosity import viscosity as viscosity_cls
from .specific_heat import specific_heat as specific_heat_cls
from .thermal_conductivity import thermal_conductivity as thermal_conductivity_cls
from .molecular_weight import molecular_weight as molecular_weight_cls
from .premix_laminar_speed import premix_laminar_speed as premix_laminar_speed_cls
from .premix_critical_strain import premix_critical_strain as premix_critical_strain_cls
from .premix_unburnt_temp import premix_unburnt_temp as premix_unburnt_temp_cls
from .premix_unburnt_density import premix_unburnt_density as premix_unburnt_density_cls
from .premix_heat_trans_coeff import premix_heat_trans_coeff as premix_heat_trans_coeff_cls
from .premix_heat_of_comb import premix_heat_of_comb as premix_heat_of_comb_cls
from .premix_unburnt_fuel_mf import premix_unburnt_fuel_mf as premix_unburnt_fuel_mf_cls
from .premix_adiabatic_temp import premix_adiabatic_temp as premix_adiabatic_temp_cls
from .therm_exp_coeff import therm_exp_coeff as therm_exp_coeff_cls
from .characteristic_vibrational_temperature import characteristic_vibrational_temperature as characteristic_vibrational_temperature_cls
from .absorption_coefficient import absorption_coefficient as absorption_coefficient_cls
from .melting_heat import melting_heat as melting_heat_cls
from .tsolidus import tsolidus as tsolidus_cls
from .tliqidus import tliqidus as tliqidus_cls
from .liquidus_slope import liquidus_slope as liquidus_slope_cls
from .partition_coeff import partition_coeff as partition_coeff_cls
from .eutectic_mf import eutectic_mf as eutectic_mf_cls
from .solid_diffusion import solid_diffusion as solid_diffusion_cls
from .solut_exp_coeff import solut_exp_coeff as solut_exp_coeff_cls
from .scattering_coefficient import scattering_coefficient as scattering_coefficient_cls
from .scattering_phase_function import scattering_phase_function as scattering_phase_function_cls
from .refractive_index import refractive_index as refractive_index_cls
from .formation_entropy import formation_entropy as formation_entropy_cls
from .formation_enthalpy import formation_enthalpy as formation_enthalpy_cls
from .reference_temperature_1 import reference_temperature as reference_temperature_cls
from .lennard_jones_length import lennard_jones_length as lennard_jones_length_cls
from .lennard_jones_energy import lennard_jones_energy as lennard_jones_energy_cls
from .thermal_accom_coefficient import thermal_accom_coefficient as thermal_accom_coefficient_cls
from .velocity_accom_coefficient import velocity_accom_coefficient as velocity_accom_coefficient_cls
from .degrees_of_freedom import degrees_of_freedom as degrees_of_freedom_cls
from .uds_diffusivity import uds_diffusivity as uds_diffusivity_cls
from .electric_conductivity import electric_conductivity as electric_conductivity_cls
from .dual_electric_conductivity import dual_electric_conductivity as dual_electric_conductivity_cls
from .lithium_diffusivity import lithium_diffusivity as lithium_diffusivity_cls
from .magnetic_permeability import magnetic_permeability as magnetic_permeability_cls
from .speed_of_sound import speed_of_sound as speed_of_sound_cls
from .critical_temperature import critical_temperature as critical_temperature_cls
from .critical_pressure import critical_pressure as critical_pressure_cls
from .critical_volume import critical_volume as critical_volume_cls
from .acentric_factor import acentric_factor as acentric_factor_cls
from .latent_heat import latent_heat as latent_heat_cls
from .saturation_pressure import saturation_pressure as saturation_pressure_cls
from .vaporization_temperature import vaporization_temperature as vaporization_temperature_cls
from .charge import charge as charge_cls
class fluid_child(Group):
    """
    'child_object_type' of fluid.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'chemical_formula', 'density', 'viscosity', 'specific_heat',
         'thermal_conductivity', 'molecular_weight', 'premix_laminar_speed',
         'premix_critical_strain', 'premix_unburnt_temp',
         'premix_unburnt_density', 'premix_heat_trans_coeff',
         'premix_heat_of_comb', 'premix_unburnt_fuel_mf',
         'premix_adiabatic_temp', 'therm_exp_coeff',
         'characteristic_vibrational_temperature', 'absorption_coefficient',
         'melting_heat', 'tsolidus', 'tliqidus', 'liquidus_slope',
         'partition_coeff', 'eutectic_mf', 'solid_diffusion',
         'solut_exp_coeff', 'scattering_coefficient',
         'scattering_phase_function', 'refractive_index', 'formation_entropy',
         'formation_enthalpy', 'reference_temperature',
         'lennard_jones_length', 'lennard_jones_energy',
         'thermal_accom_coefficient', 'velocity_accom_coefficient',
         'degrees_of_freedom', 'uds_diffusivity', 'electric_conductivity',
         'dual_electric_conductivity', 'lithium_diffusivity',
         'magnetic_permeability', 'speed_of_sound', 'critical_temperature',
         'critical_pressure', 'critical_volume', 'acentric_factor',
         'latent_heat', 'saturation_pressure', 'vaporization_temperature',
         'charge']

    name: name_cls = name_cls
    """
    name child of fluid_child.
    """
    chemical_formula: chemical_formula_cls = chemical_formula_cls
    """
    chemical_formula child of fluid_child.
    """
    density: density_cls = density_cls
    """
    density child of fluid_child.
    """
    viscosity: viscosity_cls = viscosity_cls
    """
    viscosity child of fluid_child.
    """
    specific_heat: specific_heat_cls = specific_heat_cls
    """
    specific_heat child of fluid_child.
    """
    thermal_conductivity: thermal_conductivity_cls = thermal_conductivity_cls
    """
    thermal_conductivity child of fluid_child.
    """
    molecular_weight: molecular_weight_cls = molecular_weight_cls
    """
    molecular_weight child of fluid_child.
    """
    premix_laminar_speed: premix_laminar_speed_cls = premix_laminar_speed_cls
    """
    premix_laminar_speed child of fluid_child.
    """
    premix_critical_strain: premix_critical_strain_cls = premix_critical_strain_cls
    """
    premix_critical_strain child of fluid_child.
    """
    premix_unburnt_temp: premix_unburnt_temp_cls = premix_unburnt_temp_cls
    """
    premix_unburnt_temp child of fluid_child.
    """
    premix_unburnt_density: premix_unburnt_density_cls = premix_unburnt_density_cls
    """
    premix_unburnt_density child of fluid_child.
    """
    premix_heat_trans_coeff: premix_heat_trans_coeff_cls = premix_heat_trans_coeff_cls
    """
    premix_heat_trans_coeff child of fluid_child.
    """
    premix_heat_of_comb: premix_heat_of_comb_cls = premix_heat_of_comb_cls
    """
    premix_heat_of_comb child of fluid_child.
    """
    premix_unburnt_fuel_mf: premix_unburnt_fuel_mf_cls = premix_unburnt_fuel_mf_cls
    """
    premix_unburnt_fuel_mf child of fluid_child.
    """
    premix_adiabatic_temp: premix_adiabatic_temp_cls = premix_adiabatic_temp_cls
    """
    premix_adiabatic_temp child of fluid_child.
    """
    therm_exp_coeff: therm_exp_coeff_cls = therm_exp_coeff_cls
    """
    therm_exp_coeff child of fluid_child.
    """
    characteristic_vibrational_temperature: characteristic_vibrational_temperature_cls = characteristic_vibrational_temperature_cls
    """
    characteristic_vibrational_temperature child of fluid_child.
    """
    absorption_coefficient: absorption_coefficient_cls = absorption_coefficient_cls
    """
    absorption_coefficient child of fluid_child.
    """
    melting_heat: melting_heat_cls = melting_heat_cls
    """
    melting_heat child of fluid_child.
    """
    tsolidus: tsolidus_cls = tsolidus_cls
    """
    tsolidus child of fluid_child.
    """
    tliqidus: tliqidus_cls = tliqidus_cls
    """
    tliqidus child of fluid_child.
    """
    liquidus_slope: liquidus_slope_cls = liquidus_slope_cls
    """
    liquidus_slope child of fluid_child.
    """
    partition_coeff: partition_coeff_cls = partition_coeff_cls
    """
    partition_coeff child of fluid_child.
    """
    eutectic_mf: eutectic_mf_cls = eutectic_mf_cls
    """
    eutectic_mf child of fluid_child.
    """
    solid_diffusion: solid_diffusion_cls = solid_diffusion_cls
    """
    solid_diffusion child of fluid_child.
    """
    solut_exp_coeff: solut_exp_coeff_cls = solut_exp_coeff_cls
    """
    solut_exp_coeff child of fluid_child.
    """
    scattering_coefficient: scattering_coefficient_cls = scattering_coefficient_cls
    """
    scattering_coefficient child of fluid_child.
    """
    scattering_phase_function: scattering_phase_function_cls = scattering_phase_function_cls
    """
    scattering_phase_function child of fluid_child.
    """
    refractive_index: refractive_index_cls = refractive_index_cls
    """
    refractive_index child of fluid_child.
    """
    formation_entropy: formation_entropy_cls = formation_entropy_cls
    """
    formation_entropy child of fluid_child.
    """
    formation_enthalpy: formation_enthalpy_cls = formation_enthalpy_cls
    """
    formation_enthalpy child of fluid_child.
    """
    reference_temperature: reference_temperature_cls = reference_temperature_cls
    """
    reference_temperature child of fluid_child.
    """
    lennard_jones_length: lennard_jones_length_cls = lennard_jones_length_cls
    """
    lennard_jones_length child of fluid_child.
    """
    lennard_jones_energy: lennard_jones_energy_cls = lennard_jones_energy_cls
    """
    lennard_jones_energy child of fluid_child.
    """
    thermal_accom_coefficient: thermal_accom_coefficient_cls = thermal_accom_coefficient_cls
    """
    thermal_accom_coefficient child of fluid_child.
    """
    velocity_accom_coefficient: velocity_accom_coefficient_cls = velocity_accom_coefficient_cls
    """
    velocity_accom_coefficient child of fluid_child.
    """
    degrees_of_freedom: degrees_of_freedom_cls = degrees_of_freedom_cls
    """
    degrees_of_freedom child of fluid_child.
    """
    uds_diffusivity: uds_diffusivity_cls = uds_diffusivity_cls
    """
    uds_diffusivity child of fluid_child.
    """
    electric_conductivity: electric_conductivity_cls = electric_conductivity_cls
    """
    electric_conductivity child of fluid_child.
    """
    dual_electric_conductivity: dual_electric_conductivity_cls = dual_electric_conductivity_cls
    """
    dual_electric_conductivity child of fluid_child.
    """
    lithium_diffusivity: lithium_diffusivity_cls = lithium_diffusivity_cls
    """
    lithium_diffusivity child of fluid_child.
    """
    magnetic_permeability: magnetic_permeability_cls = magnetic_permeability_cls
    """
    magnetic_permeability child of fluid_child.
    """
    speed_of_sound: speed_of_sound_cls = speed_of_sound_cls
    """
    speed_of_sound child of fluid_child.
    """
    critical_temperature: critical_temperature_cls = critical_temperature_cls
    """
    critical_temperature child of fluid_child.
    """
    critical_pressure: critical_pressure_cls = critical_pressure_cls
    """
    critical_pressure child of fluid_child.
    """
    critical_volume: critical_volume_cls = critical_volume_cls
    """
    critical_volume child of fluid_child.
    """
    acentric_factor: acentric_factor_cls = acentric_factor_cls
    """
    acentric_factor child of fluid_child.
    """
    latent_heat: latent_heat_cls = latent_heat_cls
    """
    latent_heat child of fluid_child.
    """
    saturation_pressure: saturation_pressure_cls = saturation_pressure_cls
    """
    saturation_pressure child of fluid_child.
    """
    vaporization_temperature: vaporization_temperature_cls = vaporization_temperature_cls
    """
    vaporization_temperature child of fluid_child.
    """
    charge: charge_cls = charge_cls
    """
    charge child of fluid_child.
    """
