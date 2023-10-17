#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .limiter_type import limiter_type as limiter_type_cls
from .cell_to_limiting import cell_to_limiting as cell_to_limiting_cls
from .limiter_filter import limiter_filter as limiter_filter_cls
class spatial_discretization_limiter(Group):
    """
    Enter the slope limiter set menu.
    """

    fluent_name = "spatial-discretization-limiter"

    child_names = \
        ['limiter_type', 'cell_to_limiting', 'limiter_filter']

    limiter_type: limiter_type_cls = limiter_type_cls
    """
    limiter_type child of spatial_discretization_limiter.
    """
    cell_to_limiting: cell_to_limiting_cls = cell_to_limiting_cls
    """
    cell_to_limiting child of spatial_discretization_limiter.
    """
    limiter_filter: limiter_filter_cls = limiter_filter_cls
    """
    limiter_filter child of spatial_discretization_limiter.
    """
