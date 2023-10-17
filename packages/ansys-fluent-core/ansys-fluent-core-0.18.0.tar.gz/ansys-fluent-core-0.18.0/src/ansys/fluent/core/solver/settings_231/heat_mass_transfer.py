#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .cavitation import cavitation as cavitation_cls
from .evaporation_condensation import evaporation_condensation as evaporation_condensation_cls
from .boiling import boiling as boiling_cls
from .area_density_1 import area_density as area_density_cls
from .alternative_energy_treatment import alternative_energy_treatment as alternative_energy_treatment_cls
class heat_mass_transfer(Group):
    """
    Multiphase interphase heat and mass transfer numerics options menu.
    """

    fluent_name = "heat-mass-transfer"

    child_names = \
        ['cavitation', 'evaporation_condensation', 'boiling', 'area_density',
         'alternative_energy_treatment']

    cavitation: cavitation_cls = cavitation_cls
    """
    cavitation child of heat_mass_transfer.
    """
    evaporation_condensation: evaporation_condensation_cls = evaporation_condensation_cls
    """
    evaporation_condensation child of heat_mass_transfer.
    """
    boiling: boiling_cls = boiling_cls
    """
    boiling child of heat_mass_transfer.
    """
    area_density: area_density_cls = area_density_cls
    """
    area_density child of heat_mass_transfer.
    """
    alternative_energy_treatment: alternative_energy_treatment_cls = alternative_energy_treatment_cls
    """
    alternative_energy_treatment child of heat_mass_transfer.
    """
