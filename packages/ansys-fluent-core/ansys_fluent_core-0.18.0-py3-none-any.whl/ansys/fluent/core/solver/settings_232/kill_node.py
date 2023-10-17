#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .compute_node import compute_node as compute_node_cls
from .invalidate_case import invalidate_case as invalidate_case_cls
class kill_node(Command):
    """
    'kill_node' command.
    
    Parameters
    ----------
        compute_node : int
            'compute_node' child.
        invalidate_case : bool
            'invalidate_case' child.
    
    """

    fluent_name = "kill-node"

    argument_names = \
        ['compute_node', 'invalidate_case']

    compute_node: compute_node_cls = compute_node_cls
    """
    compute_node argument of kill_node.
    """
    invalidate_case: invalidate_case_cls = invalidate_case_cls
    """
    invalidate_case argument of kill_node.
    """
