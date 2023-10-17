#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .thread_number_control import thread_number_control as thread_number_control_cls
from .check_verbosity_1 import check_verbosity as check_verbosity_cls
from .partition_1 import partition as partition_cls
from .set_4 import set as set_cls
from .load_balance import load_balance as load_balance_cls
from .multidomain import multidomain as multidomain_cls
from .network_1 import network as network_cls
from .timer import timer as timer_cls
from .check_1 import check as check_cls
from .show_connectivity import show_connectivity as show_connectivity_cls
from .latency import latency as latency_cls
from .bandwidth import bandwidth as bandwidth_cls
class parallel(Group):
    """
    'parallel' child.
    """

    fluent_name = "parallel"

    child_names = \
        ['thread_number_control', 'check_verbosity', 'partition', 'set',
         'load_balance', 'multidomain', 'network', 'timer']

    thread_number_control: thread_number_control_cls = thread_number_control_cls
    """
    thread_number_control child of parallel.
    """
    check_verbosity: check_verbosity_cls = check_verbosity_cls
    """
    check_verbosity child of parallel.
    """
    partition: partition_cls = partition_cls
    """
    partition child of parallel.
    """
    set: set_cls = set_cls
    """
    set child of parallel.
    """
    load_balance: load_balance_cls = load_balance_cls
    """
    load_balance child of parallel.
    """
    multidomain: multidomain_cls = multidomain_cls
    """
    multidomain child of parallel.
    """
    network: network_cls = network_cls
    """
    network child of parallel.
    """
    timer: timer_cls = timer_cls
    """
    timer child of parallel.
    """
    command_names = \
        ['check', 'show_connectivity', 'latency', 'bandwidth']

    check: check_cls = check_cls
    """
    check command of parallel.
    """
    show_connectivity: show_connectivity_cls = show_connectivity_cls
    """
    show_connectivity command of parallel.
    """
    latency: latency_cls = latency_cls
    """
    latency command of parallel.
    """
    bandwidth: bandwidth_cls = bandwidth_cls
    """
    bandwidth command of parallel.
    """
