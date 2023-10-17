#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .scheme import scheme as scheme_cls
from .low_order_scheme import low_order_scheme as low_order_scheme_cls
from .high_order_scheme import high_order_scheme as high_order_scheme_cls
from .accuracy_control import accuracy_control as accuracy_control_cls
class tracking(Group):
    """
    'tracking' child.
    """

    fluent_name = "tracking"

    child_names = \
        ['scheme', 'low_order_scheme', 'high_order_scheme',
         'accuracy_control']

    scheme: scheme_cls = scheme_cls
    """
    scheme child of tracking.
    """
    low_order_scheme: low_order_scheme_cls = low_order_scheme_cls
    """
    low_order_scheme child of tracking.
    """
    high_order_scheme: high_order_scheme_cls = high_order_scheme_cls
    """
    high_order_scheme child of tracking.
    """
    accuracy_control: accuracy_control_cls = accuracy_control_cls
    """
    accuracy_control child of tracking.
    """
