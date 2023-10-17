#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .hostname import hostname as hostname_cls
from .username import username as username_cls
class spawn_node(Command):
    """
    Spawn a compute node process on a specified machine.
    
    Parameters
    ----------
        hostname : str
            'hostname' child.
        username : str
            'username' child.
    
    """

    fluent_name = "spawn-node"

    argument_names = \
        ['hostname', 'username']

    hostname: hostname_cls = hostname_cls
    """
    hostname argument of spawn_node.
    """
    username: username_cls = username_cls
    """
    username argument of spawn_node.
    """
