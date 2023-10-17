#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .viscosity_averaging import viscosity_averaging as viscosity_averaging_cls
from .turb_visc_based_damping import turb_visc_based_damping as turb_visc_based_damping_cls
from .density_func_expo import density_func_expo as density_func_expo_cls
from .density_ratio_cutoff import density_ratio_cutoff as density_ratio_cutoff_cls
from .interfacial_artificial_viscosity import interfacial_artificial_viscosity as interfacial_artificial_viscosity_cls
class viscous_flow(Group):
    """
    Multiphase viscous flow numerics options menu.
    """

    fluent_name = "viscous-flow"

    child_names = \
        ['viscosity_averaging', 'turb_visc_based_damping',
         'density_func_expo', 'density_ratio_cutoff',
         'interfacial_artificial_viscosity']

    viscosity_averaging: viscosity_averaging_cls = viscosity_averaging_cls
    """
    viscosity_averaging child of viscous_flow.
    """
    turb_visc_based_damping: turb_visc_based_damping_cls = turb_visc_based_damping_cls
    """
    turb_visc_based_damping child of viscous_flow.
    """
    density_func_expo: density_func_expo_cls = density_func_expo_cls
    """
    density_func_expo child of viscous_flow.
    """
    density_ratio_cutoff: density_ratio_cutoff_cls = density_ratio_cutoff_cls
    """
    density_ratio_cutoff child of viscous_flow.
    """
    interfacial_artificial_viscosity: interfacial_artificial_viscosity_cls = interfacial_artificial_viscosity_cls
    """
    interfacial_artificial_viscosity child of viscous_flow.
    """
