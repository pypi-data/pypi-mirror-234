#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .limiter_enabled import limiter_enabled as limiter_enabled_cls
from .report_leidenfrost_temperature import report_leidenfrost_temperature as report_leidenfrost_temperature_cls
from .offset_above_film_boiling_temperature import offset_above_film_boiling_temperature as offset_above_film_boiling_temperature_cls
class wall_film_temperature_limiter(Group):
    """
    'wall_film_temperature_limiter' child.
    """

    fluent_name = "wall-film-temperature-limiter"

    child_names = \
        ['limiter_enabled', 'report_leidenfrost_temperature',
         'offset_above_film_boiling_temperature']

    limiter_enabled: limiter_enabled_cls = limiter_enabled_cls
    """
    limiter_enabled child of wall_film_temperature_limiter.
    """
    report_leidenfrost_temperature: report_leidenfrost_temperature_cls = report_leidenfrost_temperature_cls
    """
    report_leidenfrost_temperature child of wall_film_temperature_limiter.
    """
    offset_above_film_boiling_temperature: offset_above_film_boiling_temperature_cls = offset_above_film_boiling_temperature_cls
    """
    offset_above_film_boiling_temperature child of wall_film_temperature_limiter.
    """
