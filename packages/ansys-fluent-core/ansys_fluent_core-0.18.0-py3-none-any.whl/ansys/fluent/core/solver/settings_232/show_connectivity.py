#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .compute_node import compute_node as compute_node_cls
class show_connectivity(Command):
    """
    Show machine connectivity.
    
    Parameters
    ----------
        compute_node : int
            'compute_node' child.
    
    """

    fluent_name = "show-connectivity"

    argument_names = \
        ['compute_node']

    compute_node: compute_node_cls = compute_node_cls
    """
    compute_node argument of show_connectivity.
    """
