#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .use_multi_physics import use_multi_physics as use_multi_physics_cls
from .threshold import threshold as threshold_cls
from .interval import interval as interval_cls
class physical_models(Group):
    """
    Use physical-models load balancing?.
    """

    fluent_name = "physical-models"

    child_names = \
        ['use_multi_physics', 'threshold', 'interval']

    use_multi_physics: use_multi_physics_cls = use_multi_physics_cls
    """
    use_multi_physics child of physical_models.
    """
    threshold: threshold_cls = threshold_cls
    """
    threshold child of physical_models.
    """
    interval: interval_cls = interval_cls
    """
    interval child of physical_models.
    """
