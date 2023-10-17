#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .auto_1 import auto as auto_cls
from .set_3 import set as set_cls
from .combine_partition import combine_partition as combine_partition_cls
from .merge_clusters import merge_clusters as merge_clusters_cls
from .method_5 import method as method_cls
from .print_partitions import print_partitions as print_partitions_cls
from .print_active_partitions import print_active_partitions as print_active_partitions_cls
from .print_stored_partitions import print_stored_partitions as print_stored_partitions_cls
from .reorder_partitions import reorder_partitions as reorder_partitions_cls
from .reorder_partitions_to_architecture import reorder_partitions_to_architecture as reorder_partitions_to_architecture_cls
from .smooth_partition import smooth_partition as smooth_partition_cls
from .use_stored_partitions import use_stored_partitions as use_stored_partitions_cls
class partition(Group):
    """
    Enter the partition domain menu.
    """

    fluent_name = "partition"

    child_names = \
        ['auto', 'set']

    auto: auto_cls = auto_cls
    """
    auto child of partition.
    """
    set: set_cls = set_cls
    """
    set child of partition.
    """
    command_names = \
        ['combine_partition', 'merge_clusters', 'method', 'print_partitions',
         'print_active_partitions', 'print_stored_partitions',
         'reorder_partitions', 'reorder_partitions_to_architecture',
         'smooth_partition', 'use_stored_partitions']

    combine_partition: combine_partition_cls = combine_partition_cls
    """
    combine_partition command of partition.
    """
    merge_clusters: merge_clusters_cls = merge_clusters_cls
    """
    merge_clusters command of partition.
    """
    method: method_cls = method_cls
    """
    method command of partition.
    """
    print_partitions: print_partitions_cls = print_partitions_cls
    """
    print_partitions command of partition.
    """
    print_active_partitions: print_active_partitions_cls = print_active_partitions_cls
    """
    print_active_partitions command of partition.
    """
    print_stored_partitions: print_stored_partitions_cls = print_stored_partitions_cls
    """
    print_stored_partitions command of partition.
    """
    reorder_partitions: reorder_partitions_cls = reorder_partitions_cls
    """
    reorder_partitions command of partition.
    """
    reorder_partitions_to_architecture: reorder_partitions_to_architecture_cls = reorder_partitions_to_architecture_cls
    """
    reorder_partitions_to_architecture command of partition.
    """
    smooth_partition: smooth_partition_cls = smooth_partition_cls
    """
    smooth_partition command of partition.
    """
    use_stored_partitions: use_stored_partitions_cls = use_stored_partitions_cls
    """
    use_stored_partitions command of partition.
    """
