#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .species import species as species_cls
from .reactions import reactions as reactions_cls
from .reaction_mechs import reaction_mechs as reaction_mechs_cls
from .density import density as density_cls
from .specific_heat import specific_heat as specific_heat_cls
from .thermal_conductivity import thermal_conductivity as thermal_conductivity_cls
from .viscosity import viscosity as viscosity_cls
from .molecular_weight import molecular_weight as molecular_weight_cls
from .mass_diffusivity import mass_diffusivity as mass_diffusivity_cls
from .thermal_diffusivity import thermal_diffusivity as thermal_diffusivity_cls
from .formation_enthalpy import formation_enthalpy as formation_enthalpy_cls
from .formation_entropy import formation_entropy as formation_entropy_cls
from .characteristic_vibrational_temperature import characteristic_vibrational_temperature as characteristic_vibrational_temperature_cls
from .reference_temperature import reference_temperature as reference_temperature_cls
from .lennard_jones_length import lennard_jones_length as lennard_jones_length_cls
from .lennard_jones_energy import lennard_jones_energy as lennard_jones_energy_cls
from .thermal_accom_coefficient import thermal_accom_coefficient as thermal_accom_coefficient_cls
from .velocity_accom_coefficient import velocity_accom_coefficient as velocity_accom_coefficient_cls
from .absorption_coefficient import absorption_coefficient as absorption_coefficient_cls
from .scattering_coefficient import scattering_coefficient as scattering_coefficient_cls
from .scattering_phase_function import scattering_phase_function as scattering_phase_function_cls
from .therm_exp_coeff import therm_exp_coeff as therm_exp_coeff_cls
from .premix_unburnt_density import premix_unburnt_density as premix_unburnt_density_cls
from .premix_unburnt_temp import premix_unburnt_temp as premix_unburnt_temp_cls
from .premix_adiabatic_temp import premix_adiabatic_temp as premix_adiabatic_temp_cls
from .premix_unburnt_cp import premix_unburnt_cp as premix_unburnt_cp_cls
from .premix_heat_trans_coeff import premix_heat_trans_coeff as premix_heat_trans_coeff_cls
from .premix_laminar_speed import premix_laminar_speed as premix_laminar_speed_cls
from .premix_laminar_thickness import premix_laminar_thickness as premix_laminar_thickness_cls
from .premix_critical_strain import premix_critical_strain as premix_critical_strain_cls
from .premix_heat_of_comb import premix_heat_of_comb as premix_heat_of_comb_cls
from .premix_unburnt_fuel_mf import premix_unburnt_fuel_mf as premix_unburnt_fuel_mf_cls
from .refractive_index import refractive_index as refractive_index_cls
from .latent_heat import latent_heat as latent_heat_cls
from .thermophoretic_co import thermophoretic_co as thermophoretic_co_cls
from .vaporization_temperature import vaporization_temperature as vaporization_temperature_cls
from .boiling_point import boiling_point as boiling_point_cls
from .volatile_fraction import volatile_fraction as volatile_fraction_cls
from .binary_diffusivity import binary_diffusivity as binary_diffusivity_cls
from .diffusivity_reference_pressure import diffusivity_reference_pressure as diffusivity_reference_pressure_cls
from .vapor_pressure import vapor_pressure as vapor_pressure_cls
from .degrees_of_freedom import degrees_of_freedom as degrees_of_freedom_cls
from .emissivity import emissivity as emissivity_cls
from .scattering_factor import scattering_factor as scattering_factor_cls
from .heat_of_pyrolysis import heat_of_pyrolysis as heat_of_pyrolysis_cls
from .swelling_coefficient import swelling_coefficient as swelling_coefficient_cls
from .burn_stoichiometry import burn_stoichiometry as burn_stoichiometry_cls
from .combustible_fraction import combustible_fraction as combustible_fraction_cls
from .burn_hreact import burn_hreact as burn_hreact_cls
from .burn_hreact_fraction import burn_hreact_fraction as burn_hreact_fraction_cls
from .devolatilization_model import devolatilization_model as devolatilization_model_cls
from .combustion_model import combustion_model as combustion_model_cls
from .averaging_coefficient_t import averaging_coefficient_t as averaging_coefficient_t_cls
from .averaging_coefficient_y import averaging_coefficient_y as averaging_coefficient_y_cls
from .vaporization_model import vaporization_model as vaporization_model_cls
from .thermolysis_model import thermolysis_model as thermolysis_model_cls
from .melting_heat import melting_heat as melting_heat_cls
from .tsolidus import tsolidus as tsolidus_cls
from .tliqidus import tliqidus as tliqidus_cls
from .tmelt import tmelt as tmelt_cls
from .liquidus_slope import liquidus_slope as liquidus_slope_cls
from .partition_coeff import partition_coeff as partition_coeff_cls
from .eutectic_mf import eutectic_mf as eutectic_mf_cls
from .eutectic_temp import eutectic_temp as eutectic_temp_cls
from .solut_exp_coeff import solut_exp_coeff as solut_exp_coeff_cls
from .solid_diffusion import solid_diffusion as solid_diffusion_cls
from .uds_diffusivity import uds_diffusivity as uds_diffusivity_cls
from .dpm_surften import dpm_surften as dpm_surften_cls
from .electric_conductivity import electric_conductivity as electric_conductivity_cls
from .dual_electric_conductivity import dual_electric_conductivity as dual_electric_conductivity_cls
from .lithium_diffusivity import lithium_diffusivity as lithium_diffusivity_cls
from .magnetic_permeability import magnetic_permeability as magnetic_permeability_cls
from .charge_density import charge_density as charge_density_cls
from .charge import charge as charge_cls
from .speed_of_sound import speed_of_sound as speed_of_sound_cls
from .species_phase import species_phase as species_phase_cls
from .vp_equilib import vp_equilib as vp_equilib_cls
from .critical_temperature import critical_temperature as critical_temperature_cls
from .critical_pressure import critical_pressure as critical_pressure_cls
from .critical_volume import critical_volume as critical_volume_cls
from .acentric_factor import acentric_factor as acentric_factor_cls
from .saturation_pressure import saturation_pressure as saturation_pressure_cls
from .struct_youngs_modulus import struct_youngs_modulus as struct_youngs_modulus_cls
from .struct_poisson_ratio import struct_poisson_ratio as struct_poisson_ratio_cls
from .struct_start_temperature import struct_start_temperature as struct_start_temperature_cls
from .struct_thermal_expansion import struct_thermal_expansion as struct_thermal_expansion_cls
from .atomic_number import atomic_number as atomic_number_cls
from .struct_damping_alpha import struct_damping_alpha as struct_damping_alpha_cls
from .struct_damping_beta import struct_damping_beta as struct_damping_beta_cls
class fluid_child(Group):
    """
    'child_object_type' of fluid.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['species', 'reactions', 'reaction_mechs', 'density', 'specific_heat',
         'thermal_conductivity', 'viscosity', 'molecular_weight',
         'mass_diffusivity', 'thermal_diffusivity', 'formation_enthalpy',
         'formation_entropy', 'characteristic_vibrational_temperature',
         'reference_temperature', 'lennard_jones_length',
         'lennard_jones_energy', 'thermal_accom_coefficient',
         'velocity_accom_coefficient', 'absorption_coefficient',
         'scattering_coefficient', 'scattering_phase_function',
         'therm_exp_coeff', 'premix_unburnt_density', 'premix_unburnt_temp',
         'premix_adiabatic_temp', 'premix_unburnt_cp',
         'premix_heat_trans_coeff', 'premix_laminar_speed',
         'premix_laminar_thickness', 'premix_critical_strain',
         'premix_heat_of_comb', 'premix_unburnt_fuel_mf', 'refractive_index',
         'latent_heat', 'thermophoretic_co', 'vaporization_temperature',
         'boiling_point', 'volatile_fraction', 'binary_diffusivity',
         'diffusivity_reference_pressure', 'vapor_pressure',
         'degrees_of_freedom', 'emissivity', 'scattering_factor',
         'heat_of_pyrolysis', 'swelling_coefficient', 'burn_stoichiometry',
         'combustible_fraction', 'burn_hreact', 'burn_hreact_fraction',
         'devolatilization_model', 'combustion_model',
         'averaging_coefficient_t', 'averaging_coefficient_y',
         'vaporization_model', 'thermolysis_model', 'melting_heat',
         'tsolidus', 'tliqidus', 'tmelt', 'liquidus_slope', 'partition_coeff',
         'eutectic_mf', 'eutectic_temp', 'solut_exp_coeff', 'solid_diffusion',
         'uds_diffusivity', 'dpm_surften', 'electric_conductivity',
         'dual_electric_conductivity', 'lithium_diffusivity',
         'magnetic_permeability', 'charge_density', 'charge',
         'speed_of_sound', 'species_phase', 'vp_equilib',
         'critical_temperature', 'critical_pressure', 'critical_volume',
         'acentric_factor', 'saturation_pressure', 'struct_youngs_modulus',
         'struct_poisson_ratio', 'struct_start_temperature',
         'struct_thermal_expansion', 'atomic_number', 'struct_damping_alpha',
         'struct_damping_beta']

    species: species_cls = species_cls
    """
    species child of fluid_child.
    """
    reactions: reactions_cls = reactions_cls
    """
    reactions child of fluid_child.
    """
    reaction_mechs: reaction_mechs_cls = reaction_mechs_cls
    """
    reaction_mechs child of fluid_child.
    """
    density: density_cls = density_cls
    """
    density child of fluid_child.
    """
    specific_heat: specific_heat_cls = specific_heat_cls
    """
    specific_heat child of fluid_child.
    """
    thermal_conductivity: thermal_conductivity_cls = thermal_conductivity_cls
    """
    thermal_conductivity child of fluid_child.
    """
    viscosity: viscosity_cls = viscosity_cls
    """
    viscosity child of fluid_child.
    """
    molecular_weight: molecular_weight_cls = molecular_weight_cls
    """
    molecular_weight child of fluid_child.
    """
    mass_diffusivity: mass_diffusivity_cls = mass_diffusivity_cls
    """
    mass_diffusivity child of fluid_child.
    """
    thermal_diffusivity: thermal_diffusivity_cls = thermal_diffusivity_cls
    """
    thermal_diffusivity child of fluid_child.
    """
    formation_enthalpy: formation_enthalpy_cls = formation_enthalpy_cls
    """
    formation_enthalpy child of fluid_child.
    """
    formation_entropy: formation_entropy_cls = formation_entropy_cls
    """
    formation_entropy child of fluid_child.
    """
    characteristic_vibrational_temperature: characteristic_vibrational_temperature_cls = characteristic_vibrational_temperature_cls
    """
    characteristic_vibrational_temperature child of fluid_child.
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
    absorption_coefficient: absorption_coefficient_cls = absorption_coefficient_cls
    """
    absorption_coefficient child of fluid_child.
    """
    scattering_coefficient: scattering_coefficient_cls = scattering_coefficient_cls
    """
    scattering_coefficient child of fluid_child.
    """
    scattering_phase_function: scattering_phase_function_cls = scattering_phase_function_cls
    """
    scattering_phase_function child of fluid_child.
    """
    therm_exp_coeff: therm_exp_coeff_cls = therm_exp_coeff_cls
    """
    therm_exp_coeff child of fluid_child.
    """
    premix_unburnt_density: premix_unburnt_density_cls = premix_unburnt_density_cls
    """
    premix_unburnt_density child of fluid_child.
    """
    premix_unburnt_temp: premix_unburnt_temp_cls = premix_unburnt_temp_cls
    """
    premix_unburnt_temp child of fluid_child.
    """
    premix_adiabatic_temp: premix_adiabatic_temp_cls = premix_adiabatic_temp_cls
    """
    premix_adiabatic_temp child of fluid_child.
    """
    premix_unburnt_cp: premix_unburnt_cp_cls = premix_unburnt_cp_cls
    """
    premix_unburnt_cp child of fluid_child.
    """
    premix_heat_trans_coeff: premix_heat_trans_coeff_cls = premix_heat_trans_coeff_cls
    """
    premix_heat_trans_coeff child of fluid_child.
    """
    premix_laminar_speed: premix_laminar_speed_cls = premix_laminar_speed_cls
    """
    premix_laminar_speed child of fluid_child.
    """
    premix_laminar_thickness: premix_laminar_thickness_cls = premix_laminar_thickness_cls
    """
    premix_laminar_thickness child of fluid_child.
    """
    premix_critical_strain: premix_critical_strain_cls = premix_critical_strain_cls
    """
    premix_critical_strain child of fluid_child.
    """
    premix_heat_of_comb: premix_heat_of_comb_cls = premix_heat_of_comb_cls
    """
    premix_heat_of_comb child of fluid_child.
    """
    premix_unburnt_fuel_mf: premix_unburnt_fuel_mf_cls = premix_unburnt_fuel_mf_cls
    """
    premix_unburnt_fuel_mf child of fluid_child.
    """
    refractive_index: refractive_index_cls = refractive_index_cls
    """
    refractive_index child of fluid_child.
    """
    latent_heat: latent_heat_cls = latent_heat_cls
    """
    latent_heat child of fluid_child.
    """
    thermophoretic_co: thermophoretic_co_cls = thermophoretic_co_cls
    """
    thermophoretic_co child of fluid_child.
    """
    vaporization_temperature: vaporization_temperature_cls = vaporization_temperature_cls
    """
    vaporization_temperature child of fluid_child.
    """
    boiling_point: boiling_point_cls = boiling_point_cls
    """
    boiling_point child of fluid_child.
    """
    volatile_fraction: volatile_fraction_cls = volatile_fraction_cls
    """
    volatile_fraction child of fluid_child.
    """
    binary_diffusivity: binary_diffusivity_cls = binary_diffusivity_cls
    """
    binary_diffusivity child of fluid_child.
    """
    diffusivity_reference_pressure: diffusivity_reference_pressure_cls = diffusivity_reference_pressure_cls
    """
    diffusivity_reference_pressure child of fluid_child.
    """
    vapor_pressure: vapor_pressure_cls = vapor_pressure_cls
    """
    vapor_pressure child of fluid_child.
    """
    degrees_of_freedom: degrees_of_freedom_cls = degrees_of_freedom_cls
    """
    degrees_of_freedom child of fluid_child.
    """
    emissivity: emissivity_cls = emissivity_cls
    """
    emissivity child of fluid_child.
    """
    scattering_factor: scattering_factor_cls = scattering_factor_cls
    """
    scattering_factor child of fluid_child.
    """
    heat_of_pyrolysis: heat_of_pyrolysis_cls = heat_of_pyrolysis_cls
    """
    heat_of_pyrolysis child of fluid_child.
    """
    swelling_coefficient: swelling_coefficient_cls = swelling_coefficient_cls
    """
    swelling_coefficient child of fluid_child.
    """
    burn_stoichiometry: burn_stoichiometry_cls = burn_stoichiometry_cls
    """
    burn_stoichiometry child of fluid_child.
    """
    combustible_fraction: combustible_fraction_cls = combustible_fraction_cls
    """
    combustible_fraction child of fluid_child.
    """
    burn_hreact: burn_hreact_cls = burn_hreact_cls
    """
    burn_hreact child of fluid_child.
    """
    burn_hreact_fraction: burn_hreact_fraction_cls = burn_hreact_fraction_cls
    """
    burn_hreact_fraction child of fluid_child.
    """
    devolatilization_model: devolatilization_model_cls = devolatilization_model_cls
    """
    devolatilization_model child of fluid_child.
    """
    combustion_model: combustion_model_cls = combustion_model_cls
    """
    combustion_model child of fluid_child.
    """
    averaging_coefficient_t: averaging_coefficient_t_cls = averaging_coefficient_t_cls
    """
    averaging_coefficient_t child of fluid_child.
    """
    averaging_coefficient_y: averaging_coefficient_y_cls = averaging_coefficient_y_cls
    """
    averaging_coefficient_y child of fluid_child.
    """
    vaporization_model: vaporization_model_cls = vaporization_model_cls
    """
    vaporization_model child of fluid_child.
    """
    thermolysis_model: thermolysis_model_cls = thermolysis_model_cls
    """
    thermolysis_model child of fluid_child.
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
    tmelt: tmelt_cls = tmelt_cls
    """
    tmelt child of fluid_child.
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
    eutectic_temp: eutectic_temp_cls = eutectic_temp_cls
    """
    eutectic_temp child of fluid_child.
    """
    solut_exp_coeff: solut_exp_coeff_cls = solut_exp_coeff_cls
    """
    solut_exp_coeff child of fluid_child.
    """
    solid_diffusion: solid_diffusion_cls = solid_diffusion_cls
    """
    solid_diffusion child of fluid_child.
    """
    uds_diffusivity: uds_diffusivity_cls = uds_diffusivity_cls
    """
    uds_diffusivity child of fluid_child.
    """
    dpm_surften: dpm_surften_cls = dpm_surften_cls
    """
    dpm_surften child of fluid_child.
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
    charge_density: charge_density_cls = charge_density_cls
    """
    charge_density child of fluid_child.
    """
    charge: charge_cls = charge_cls
    """
    charge child of fluid_child.
    """
    speed_of_sound: speed_of_sound_cls = speed_of_sound_cls
    """
    speed_of_sound child of fluid_child.
    """
    species_phase: species_phase_cls = species_phase_cls
    """
    species_phase child of fluid_child.
    """
    vp_equilib: vp_equilib_cls = vp_equilib_cls
    """
    vp_equilib child of fluid_child.
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
    saturation_pressure: saturation_pressure_cls = saturation_pressure_cls
    """
    saturation_pressure child of fluid_child.
    """
    struct_youngs_modulus: struct_youngs_modulus_cls = struct_youngs_modulus_cls
    """
    struct_youngs_modulus child of fluid_child.
    """
    struct_poisson_ratio: struct_poisson_ratio_cls = struct_poisson_ratio_cls
    """
    struct_poisson_ratio child of fluid_child.
    """
    struct_start_temperature: struct_start_temperature_cls = struct_start_temperature_cls
    """
    struct_start_temperature child of fluid_child.
    """
    struct_thermal_expansion: struct_thermal_expansion_cls = struct_thermal_expansion_cls
    """
    struct_thermal_expansion child of fluid_child.
    """
    atomic_number: atomic_number_cls = atomic_number_cls
    """
    atomic_number child of fluid_child.
    """
    struct_damping_alpha: struct_damping_alpha_cls = struct_damping_alpha_cls
    """
    struct_damping_alpha child of fluid_child.
    """
    struct_damping_beta: struct_damping_beta_cls = struct_damping_beta_cls
    """
    struct_damping_beta child of fluid_child.
    """
