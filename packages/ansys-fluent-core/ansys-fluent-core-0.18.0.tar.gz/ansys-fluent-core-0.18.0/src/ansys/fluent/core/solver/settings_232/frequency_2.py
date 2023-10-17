#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .option_14 import option as option_cls
from .iterations_1 import iterations as iterations_cls
from .time_steps import time_steps as time_steps_cls
class frequency(Group):
    """
    Define the frequency at which cells in the register are marked for poor mesh numerics treatment.
    """

    fluent_name = "frequency"

    child_names = \
        ['option', 'iterations', 'time_steps']

    option: option_cls = option_cls
    """
    option child of frequency.
    """
    iterations: iterations_cls = iterations_cls
    """
    iterations child of frequency.
    """
    time_steps: time_steps_cls = time_steps_cls
    """
    time_steps child of frequency.
    """
