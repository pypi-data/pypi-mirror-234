#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .convective_heat_transfer import convective_heat_transfer as convective_heat_transfer_cls
from .include_convective_heat_transfer import include_convective_heat_transfer as include_convective_heat_transfer_cls
from .film_movement import film_movement as film_movement_cls
from .lwf_particle_inclusion_in_dpm_concentration_enabled import lwf_particle_inclusion_in_dpm_concentration_enabled as lwf_particle_inclusion_in_dpm_concentration_enabled_cls
from .wall_film_temperature_limiter import wall_film_temperature_limiter as wall_film_temperature_limiter_cls
class wall_film(Group):
    """
    'wall_film' child.
    """

    fluent_name = "wall-film"

    child_names = \
        ['convective_heat_transfer', 'include_convective_heat_transfer',
         'film_movement',
         'lwf_particle_inclusion_in_dpm_concentration_enabled',
         'wall_film_temperature_limiter']

    convective_heat_transfer: convective_heat_transfer_cls = convective_heat_transfer_cls
    """
    convective_heat_transfer child of wall_film.
    """
    include_convective_heat_transfer: include_convective_heat_transfer_cls = include_convective_heat_transfer_cls
    """
    include_convective_heat_transfer child of wall_film.
    """
    film_movement: film_movement_cls = film_movement_cls
    """
    film_movement child of wall_film.
    """
    lwf_particle_inclusion_in_dpm_concentration_enabled: lwf_particle_inclusion_in_dpm_concentration_enabled_cls = lwf_particle_inclusion_in_dpm_concentration_enabled_cls
    """
    lwf_particle_inclusion_in_dpm_concentration_enabled child of wall_film.
    """
    wall_film_temperature_limiter: wall_film_temperature_limiter_cls = wall_film_temperature_limiter_cls
    """
    wall_film_temperature_limiter child of wall_film.
    """
