#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .mass_flow_1 import mass_flow as mass_flow_cls
from .heat_transfer_1 import heat_transfer as heat_transfer_cls
from .heat_transfer_sensible import heat_transfer_sensible as heat_transfer_sensible_cls
from .rad_heat_trans import rad_heat_trans as rad_heat_trans_cls
from .film_mass_flow import film_mass_flow as film_mass_flow_cls
from .film_heat_transfer import film_heat_transfer as film_heat_transfer_cls
from .pressure_work_1 import pressure_work as pressure_work_cls
from .viscous_work import viscous_work as viscous_work_cls
class fluxes(Group):
    """
    'fluxes' child.
    """

    fluent_name = "fluxes"

    command_names = \
        ['mass_flow', 'heat_transfer', 'heat_transfer_sensible',
         'rad_heat_trans', 'film_mass_flow', 'film_heat_transfer',
         'pressure_work', 'viscous_work']

    mass_flow: mass_flow_cls = mass_flow_cls
    """
    mass_flow command of fluxes.
    """
    heat_transfer: heat_transfer_cls = heat_transfer_cls
    """
    heat_transfer command of fluxes.
    """
    heat_transfer_sensible: heat_transfer_sensible_cls = heat_transfer_sensible_cls
    """
    heat_transfer_sensible command of fluxes.
    """
    rad_heat_trans: rad_heat_trans_cls = rad_heat_trans_cls
    """
    rad_heat_trans command of fluxes.
    """
    film_mass_flow: film_mass_flow_cls = film_mass_flow_cls
    """
    film_mass_flow command of fluxes.
    """
    film_heat_transfer: film_heat_transfer_cls = film_heat_transfer_cls
    """
    film_heat_transfer command of fluxes.
    """
    pressure_work: pressure_work_cls = pressure_work_cls
    """
    pressure_work command of fluxes.
    """
    viscous_work: viscous_work_cls = viscous_work_cls
    """
    viscous_work command of fluxes.
    """
