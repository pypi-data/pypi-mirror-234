#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .option import option as option_cls
from .random_eddy_lifetime import random_eddy_lifetime as random_eddy_lifetime_cls
from .number_of_tries import number_of_tries as number_of_tries_cls
from .time_scale_constant_1 import time_scale_constant as time_scale_constant_cls
class turbulent_dispersion(Group):
    """
    'turbulent_dispersion' child.
    """

    fluent_name = "turbulent-dispersion"

    child_names = \
        ['option', 'random_eddy_lifetime', 'number_of_tries',
         'time_scale_constant']

    option: option_cls = option_cls
    """
    option child of turbulent_dispersion.
    """
    random_eddy_lifetime: random_eddy_lifetime_cls = random_eddy_lifetime_cls
    """
    random_eddy_lifetime child of turbulent_dispersion.
    """
    number_of_tries: number_of_tries_cls = number_of_tries_cls
    """
    number_of_tries child of turbulent_dispersion.
    """
    time_scale_constant: time_scale_constant_cls = time_scale_constant_cls
    """
    time_scale_constant child of turbulent_dispersion.
    """
