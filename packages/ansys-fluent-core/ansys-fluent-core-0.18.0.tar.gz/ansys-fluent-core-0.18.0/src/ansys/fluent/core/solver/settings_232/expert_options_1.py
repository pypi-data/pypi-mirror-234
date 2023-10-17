#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .re_randomization_every_iteration_enabled import re_randomization_every_iteration_enabled as re_randomization_every_iteration_enabled_cls
from .re_randomization_every_timestep_enabled import re_randomization_every_timestep_enabled as re_randomization_every_timestep_enabled_cls
from .tracking_statistics_format import tracking_statistics_format as tracking_statistics_format_cls
from .verbosity_1 import verbosity as verbosity_cls
class expert_options(Group):
    """
    Menu containing not frequently used (expert level) settings.
    """

    fluent_name = "expert-options"

    child_names = \
        ['re_randomization_every_iteration_enabled',
         're_randomization_every_timestep_enabled',
         'tracking_statistics_format', 'verbosity']

    re_randomization_every_iteration_enabled: re_randomization_every_iteration_enabled_cls = re_randomization_every_iteration_enabled_cls
    """
    re_randomization_every_iteration_enabled child of expert_options.
    """
    re_randomization_every_timestep_enabled: re_randomization_every_timestep_enabled_cls = re_randomization_every_timestep_enabled_cls
    """
    re_randomization_every_timestep_enabled child of expert_options.
    """
    tracking_statistics_format: tracking_statistics_format_cls = tracking_statistics_format_cls
    """
    tracking_statistics_format child of expert_options.
    """
    verbosity: verbosity_cls = verbosity_cls
    """
    verbosity child of expert_options.
    """
