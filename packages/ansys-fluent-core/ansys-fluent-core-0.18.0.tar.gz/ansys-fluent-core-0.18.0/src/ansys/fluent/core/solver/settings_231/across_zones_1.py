#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .across_zone_boundaries import across_zone_boundaries as across_zone_boundaries_cls
class across_zones(Command):
    """
    Enable partitioning by zone or by domain.
    
    Parameters
    ----------
        across_zone_boundaries : bool
            'across_zone_boundaries' child.
    
    """

    fluent_name = "across-zones"

    argument_names = \
        ['across_zone_boundaries']

    across_zone_boundaries: across_zone_boundaries_cls = across_zone_boundaries_cls
    """
    across_zone_boundaries argument of across_zones.
    """
