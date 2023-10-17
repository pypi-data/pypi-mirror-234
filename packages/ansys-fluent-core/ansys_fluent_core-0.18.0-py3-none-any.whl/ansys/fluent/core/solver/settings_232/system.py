#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .proc_statistics import proc_statistics as proc_statistics_cls
from .sys_statistics import sys_statistics as sys_statistics_cls
from .gpgpu_statistics import gpgpu_statistics as gpgpu_statistics_cls
from .time_statistics import time_statistics as time_statistics_cls
class system(Group):
    """
    'system' child.
    """

    fluent_name = "system"

    command_names = \
        ['proc_statistics', 'sys_statistics', 'gpgpu_statistics',
         'time_statistics']

    proc_statistics: proc_statistics_cls = proc_statistics_cls
    """
    proc_statistics command of system.
    """
    sys_statistics: sys_statistics_cls = sys_statistics_cls
    """
    sys_statistics command of system.
    """
    gpgpu_statistics: gpgpu_statistics_cls = gpgpu_statistics_cls
    """
    gpgpu_statistics command of system.
    """
    time_statistics: time_statistics_cls = time_statistics_cls
    """
    time_statistics command of system.
    """
