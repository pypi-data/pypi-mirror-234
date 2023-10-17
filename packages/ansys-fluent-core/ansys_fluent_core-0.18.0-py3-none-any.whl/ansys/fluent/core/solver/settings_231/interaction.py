#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .option import option as option_cls
from .update_sources_every_flow_iteration import update_sources_every_flow_iteration as update_sources_every_flow_iteration_cls
from .iteration_interval import iteration_interval as iteration_interval_cls
class interaction(Group):
    """
    'interaction' child.
    """

    fluent_name = "interaction"

    child_names = \
        ['option', 'update_sources_every_flow_iteration',
         'iteration_interval']

    option: option_cls = option_cls
    """
    option child of interaction.
    """
    update_sources_every_flow_iteration: update_sources_every_flow_iteration_cls = update_sources_every_flow_iteration_cls
    """
    update_sources_every_flow_iteration child of interaction.
    """
    iteration_interval: iteration_interval_cls = iteration_interval_cls
    """
    iteration_interval child of interaction.
    """
