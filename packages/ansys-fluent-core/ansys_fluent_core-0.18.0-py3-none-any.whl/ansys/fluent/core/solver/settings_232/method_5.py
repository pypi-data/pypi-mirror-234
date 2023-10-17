#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .partition_method import partition_method as partition_method_cls
from .count import count as count_cls
class method(Command):
    """
    Partition the domain.
    
    Parameters
    ----------
        partition_method : str
            'partition_method' child.
        count : int
            'count' child.
    
    """

    fluent_name = "method"

    argument_names = \
        ['partition_method', 'count']

    partition_method: partition_method_cls = partition_method_cls
    """
    partition_method argument of method.
    """
    count: count_cls = count_cls
    """
    count argument of method.
    """
