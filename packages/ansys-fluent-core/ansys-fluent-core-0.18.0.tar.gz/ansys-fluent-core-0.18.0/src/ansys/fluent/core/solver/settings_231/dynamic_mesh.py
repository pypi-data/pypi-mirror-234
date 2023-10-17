#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .use import use as use_cls
from .auto_1 import auto as auto_cls
from .threshold import threshold as threshold_cls
from .interval import interval as interval_cls
class dynamic_mesh(Group):
    """
    Use load balancing for dynamic mesh?.
    """

    fluent_name = "dynamic-mesh"

    child_names = \
        ['use', 'auto', 'threshold', 'interval']

    use: use_cls = use_cls
    """
    use child of dynamic_mesh.
    """
    auto: auto_cls = auto_cls
    """
    auto child of dynamic_mesh.
    """
    threshold: threshold_cls = threshold_cls
    """
    threshold child of dynamic_mesh.
    """
    interval: interval_cls = interval_cls
    """
    interval child of dynamic_mesh.
    """
