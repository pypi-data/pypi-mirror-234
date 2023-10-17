#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .density_1 import density as density_cls
from .specific_heat_1 import specific_heat as specific_heat_cls
from .thermal_conductivity_1 import thermal_conductivity as thermal_conductivity_cls
from .atomic_number import atomic_number as atomic_number_cls
from .absorption_coefficient import absorption_coefficient as absorption_coefficient_cls
from .scattering_coefficient_1 import scattering_coefficient as scattering_coefficient_cls
from .scattering_phase_function import scattering_phase_function as scattering_phase_function_cls
from .refractive_index import refractive_index as refractive_index_cls
from .uds_diffusivity_1 import uds_diffusivity as uds_diffusivity_cls
from .electric_conductivity import electric_conductivity as electric_conductivity_cls
from .dual_electric_conductivity import dual_electric_conductivity as dual_electric_conductivity_cls
from .lithium_diffusivity import lithium_diffusivity as lithium_diffusivity_cls
from .magnetic_permeability import magnetic_permeability as magnetic_permeability_cls
from .struct_youngs_modulus import struct_youngs_modulus as struct_youngs_modulus_cls
from .struct_poisson_ratio import struct_poisson_ratio as struct_poisson_ratio_cls
from .struct_start_temperature import struct_start_temperature as struct_start_temperature_cls
from .struct_thermal_expansion import struct_thermal_expansion as struct_thermal_expansion_cls
from .struct_damping_alpha import struct_damping_alpha as struct_damping_alpha_cls
from .struct_damping_beta import struct_damping_beta as struct_damping_beta_cls
class solid_child(Group):
    """
    'child_object_type' of solid.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['density', 'specific_heat', 'thermal_conductivity', 'atomic_number',
         'absorption_coefficient', 'scattering_coefficient',
         'scattering_phase_function', 'refractive_index', 'uds_diffusivity',
         'electric_conductivity', 'dual_electric_conductivity',
         'lithium_diffusivity', 'magnetic_permeability',
         'struct_youngs_modulus', 'struct_poisson_ratio',
         'struct_start_temperature', 'struct_thermal_expansion',
         'struct_damping_alpha', 'struct_damping_beta']

    density: density_cls = density_cls
    """
    density child of solid_child.
    """
    specific_heat: specific_heat_cls = specific_heat_cls
    """
    specific_heat child of solid_child.
    """
    thermal_conductivity: thermal_conductivity_cls = thermal_conductivity_cls
    """
    thermal_conductivity child of solid_child.
    """
    atomic_number: atomic_number_cls = atomic_number_cls
    """
    atomic_number child of solid_child.
    """
    absorption_coefficient: absorption_coefficient_cls = absorption_coefficient_cls
    """
    absorption_coefficient child of solid_child.
    """
    scattering_coefficient: scattering_coefficient_cls = scattering_coefficient_cls
    """
    scattering_coefficient child of solid_child.
    """
    scattering_phase_function: scattering_phase_function_cls = scattering_phase_function_cls
    """
    scattering_phase_function child of solid_child.
    """
    refractive_index: refractive_index_cls = refractive_index_cls
    """
    refractive_index child of solid_child.
    """
    uds_diffusivity: uds_diffusivity_cls = uds_diffusivity_cls
    """
    uds_diffusivity child of solid_child.
    """
    electric_conductivity: electric_conductivity_cls = electric_conductivity_cls
    """
    electric_conductivity child of solid_child.
    """
    dual_electric_conductivity: dual_electric_conductivity_cls = dual_electric_conductivity_cls
    """
    dual_electric_conductivity child of solid_child.
    """
    lithium_diffusivity: lithium_diffusivity_cls = lithium_diffusivity_cls
    """
    lithium_diffusivity child of solid_child.
    """
    magnetic_permeability: magnetic_permeability_cls = magnetic_permeability_cls
    """
    magnetic_permeability child of solid_child.
    """
    struct_youngs_modulus: struct_youngs_modulus_cls = struct_youngs_modulus_cls
    """
    struct_youngs_modulus child of solid_child.
    """
    struct_poisson_ratio: struct_poisson_ratio_cls = struct_poisson_ratio_cls
    """
    struct_poisson_ratio child of solid_child.
    """
    struct_start_temperature: struct_start_temperature_cls = struct_start_temperature_cls
    """
    struct_start_temperature child of solid_child.
    """
    struct_thermal_expansion: struct_thermal_expansion_cls = struct_thermal_expansion_cls
    """
    struct_thermal_expansion child of solid_child.
    """
    struct_damping_alpha: struct_damping_alpha_cls = struct_damping_alpha_cls
    """
    struct_damping_alpha child of solid_child.
    """
    struct_damping_beta: struct_damping_beta_cls = struct_damping_beta_cls
    """
    struct_damping_beta child of solid_child.
    """
