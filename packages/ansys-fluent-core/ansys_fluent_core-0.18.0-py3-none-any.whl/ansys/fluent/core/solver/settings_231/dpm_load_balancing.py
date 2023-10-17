#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .load_balancing import load_balancing as load_balancing_cls
from .threshold import threshold as threshold_cls
from .interval import interval as interval_cls
class dpm_load_balancing(Group):
    """
    Enable automatic load balancing for DPM.
    """

    fluent_name = "dpm-load-balancing"

    child_names = \
        ['load_balancing', 'threshold', 'interval']

    load_balancing: load_balancing_cls = load_balancing_cls
    """
    load_balancing child of dpm_load_balancing.
    """
    threshold: threshold_cls = threshold_cls
    """
    threshold child of dpm_load_balancing.
    """
    interval: interval_cls = interval_cls
    """
    interval child of dpm_load_balancing.
    """
