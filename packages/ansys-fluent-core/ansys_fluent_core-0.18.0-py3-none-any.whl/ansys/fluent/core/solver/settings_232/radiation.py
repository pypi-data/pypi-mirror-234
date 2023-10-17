#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .model_1 import model as model_cls
from .solar_load import solar_load as solar_load_cls
from .discrete_ordinates import discrete_ordinates as discrete_ordinates_cls
from .monte_carlo import monte_carlo as monte_carlo_cls
from .s2s import s2s as s2s_cls
from .multiband import multiband as multiband_cls
from .solve_frequency import solve_frequency as solve_frequency_cls
class radiation(Group):
    """
    'radiation' child.
    """

    fluent_name = "radiation"

    child_names = \
        ['model', 'solar_load', 'discrete_ordinates', 'monte_carlo', 's2s',
         'multiband', 'solve_frequency']

    model: model_cls = model_cls
    """
    model child of radiation.
    """
    solar_load: solar_load_cls = solar_load_cls
    """
    solar_load child of radiation.
    """
    discrete_ordinates: discrete_ordinates_cls = discrete_ordinates_cls
    """
    discrete_ordinates child of radiation.
    """
    monte_carlo: monte_carlo_cls = monte_carlo_cls
    """
    monte_carlo child of radiation.
    """
    s2s: s2s_cls = s2s_cls
    """
    s2s child of radiation.
    """
    multiband: multiband_cls = multiband_cls
    """
    multiband child of radiation.
    """
    solve_frequency: solve_frequency_cls = solve_frequency_cls
    """
    solve_frequency child of radiation.
    """
