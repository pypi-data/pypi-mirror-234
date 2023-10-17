#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .partition_mask import partition_mask as partition_mask_cls
from .verbosity_12 import verbosity as verbosity_cls
from .time_out import time_out as time_out_cls
from .fast_io import fast_io as fast_io_cls
class set(Group):
    """
    'set' child.
    """

    fluent_name = "set"

    child_names = \
        ['partition_mask', 'verbosity', 'time_out', 'fast_io']

    partition_mask: partition_mask_cls = partition_mask_cls
    """
    partition_mask child of set.
    """
    verbosity: verbosity_cls = verbosity_cls
    """
    verbosity child of set.
    """
    time_out: time_out_cls = time_out_cls
    """
    time_out child of set.
    """
    fast_io: fast_io_cls = fast_io_cls
    """
    fast_io child of set.
    """
