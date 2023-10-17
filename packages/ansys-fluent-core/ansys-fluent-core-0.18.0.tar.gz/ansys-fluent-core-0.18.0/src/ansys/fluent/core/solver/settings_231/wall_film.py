#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .include_convective_heat_transfer import include_convective_heat_transfer as include_convective_heat_transfer_cls
from .include_lwf_particles_in_dpm_concentration import include_lwf_particles_in_dpm_concentration as include_lwf_particles_in_dpm_concentration_cls
from .wall_film_temperature_limiter import wall_film_temperature_limiter as wall_film_temperature_limiter_cls
class wall_film(Group):
    """
    'wall_film' child.
    """

    fluent_name = "wall-film"

    child_names = \
        ['include_convective_heat_transfer',
         'include_lwf_particles_in_dpm_concentration',
         'wall_film_temperature_limiter']

    include_convective_heat_transfer: include_convective_heat_transfer_cls = include_convective_heat_transfer_cls
    """
    include_convective_heat_transfer child of wall_film.
    """
    include_lwf_particles_in_dpm_concentration: include_lwf_particles_in_dpm_concentration_cls = include_lwf_particles_in_dpm_concentration_cls
    """
    include_lwf_particles_in_dpm_concentration child of wall_film.
    """
    wall_film_temperature_limiter: wall_film_temperature_limiter_cls = wall_film_temperature_limiter_cls
    """
    wall_film_temperature_limiter child of wall_film.
    """
