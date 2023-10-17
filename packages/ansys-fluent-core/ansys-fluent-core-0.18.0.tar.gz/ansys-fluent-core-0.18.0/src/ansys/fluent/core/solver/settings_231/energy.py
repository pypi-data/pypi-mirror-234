#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .enabled import enabled as enabled_cls
from .viscous_dissipation import viscous_dissipation as viscous_dissipation_cls
from .pressure_work import pressure_work as pressure_work_cls
from .kinetic_energy import kinetic_energy as kinetic_energy_cls
from .inlet_diffusion import inlet_diffusion as inlet_diffusion_cls
class energy(Group):
    """
    'energy' child.
    """

    fluent_name = "energy"

    child_names = \
        ['enabled', 'viscous_dissipation', 'pressure_work', 'kinetic_energy',
         'inlet_diffusion']

    enabled: enabled_cls = enabled_cls
    """
    enabled child of energy.
    """
    viscous_dissipation: viscous_dissipation_cls = viscous_dissipation_cls
    """
    viscous_dissipation child of energy.
    """
    pressure_work: pressure_work_cls = pressure_work_cls
    """
    pressure_work child of energy.
    """
    kinetic_energy: kinetic_energy_cls = kinetic_energy_cls
    """
    kinetic_energy child of energy.
    """
    inlet_diffusion: inlet_diffusion_cls = inlet_diffusion_cls
    """
    inlet_diffusion child of energy.
    """
