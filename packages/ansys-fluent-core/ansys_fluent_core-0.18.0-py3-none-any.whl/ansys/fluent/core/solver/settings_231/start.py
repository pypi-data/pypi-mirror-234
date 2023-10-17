#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .address import address as address_cls
from .port import port as port_cls
class start(Command):
    """
    'start' command.
    
    Parameters
    ----------
        address : str
            'address' child.
        port : int
            'port' child.
    
    """

    fluent_name = "start"

    argument_names = \
        ['address', 'port']

    address: address_cls = address_cls
    """
    address argument of start.
    """
    port: port_cls = port_cls
    """
    port argument of start.
    """
