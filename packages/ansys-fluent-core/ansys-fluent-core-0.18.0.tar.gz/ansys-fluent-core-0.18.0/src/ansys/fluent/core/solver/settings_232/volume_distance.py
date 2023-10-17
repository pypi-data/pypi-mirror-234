#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .boundary_volume import boundary_volume as boundary_volume_cls
from .volume_growth import volume_growth as volume_growth_cls
class volume_distance(Group):
    """
    'volume_distance' child.
    """

    fluent_name = "volume-distance"

    child_names = \
        ['boundary_volume', 'volume_growth']

    boundary_volume: boundary_volume_cls = boundary_volume_cls
    """
    boundary_volume child of volume_distance.
    """
    volume_growth: volume_growth_cls = volume_growth_cls
    """
    volume_growth child of volume_distance.
    """
