#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .shell_script_path import shell_script_path as shell_script_path_cls
from .kill_all_nodes import kill_all_nodes as kill_all_nodes_cls
from .kill_node import kill_node as kill_node_cls
from .spawn_node import spawn_node as spawn_node_cls
from .load_hosts import load_hosts as load_hosts_cls
from .save_hosts import save_hosts as save_hosts_cls
class network(Group):
    """
    Enter the network configuration menu.
    """

    fluent_name = "network"

    child_names = \
        ['shell_script_path']

    shell_script_path: shell_script_path_cls = shell_script_path_cls
    """
    shell_script_path child of network.
    """
    command_names = \
        ['kill_all_nodes', 'kill_node', 'spawn_node', 'load_hosts',
         'save_hosts']

    kill_all_nodes: kill_all_nodes_cls = kill_all_nodes_cls
    """
    kill_all_nodes command of network.
    """
    kill_node: kill_node_cls = kill_node_cls
    """
    kill_node command of network.
    """
    spawn_node: spawn_node_cls = spawn_node_cls
    """
    spawn_node command of network.
    """
    load_hosts: load_hosts_cls = load_hosts_cls
    """
    load_hosts command of network.
    """
    save_hosts: save_hosts_cls = save_hosts_cls
    """
    save_hosts command of network.
    """
