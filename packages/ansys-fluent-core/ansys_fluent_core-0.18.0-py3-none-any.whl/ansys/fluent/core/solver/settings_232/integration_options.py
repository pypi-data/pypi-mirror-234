#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .absolute_ode_tolerance import absolute_ode_tolerance as absolute_ode_tolerance_cls
from .relative_ode_tolerance import relative_ode_tolerance as relative_ode_tolerance_cls
class integration_options(Group):
    """
    'integration_options' child.
    """

    fluent_name = "integration-options"

    child_names = \
        ['absolute_ode_tolerance', 'relative_ode_tolerance']

    absolute_ode_tolerance: absolute_ode_tolerance_cls = absolute_ode_tolerance_cls
    """
    absolute_ode_tolerance child of integration_options.
    """
    relative_ode_tolerance: relative_ode_tolerance_cls = relative_ode_tolerance_cls
    """
    relative_ode_tolerance child of integration_options.
    """
