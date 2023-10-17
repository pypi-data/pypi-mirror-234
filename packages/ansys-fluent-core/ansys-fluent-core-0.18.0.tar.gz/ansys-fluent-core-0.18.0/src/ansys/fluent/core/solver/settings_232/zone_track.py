#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .track_zone import track_zone as track_zone_cls
class zone_track(Group):
    """
    'zone_track' child.
    """

    fluent_name = "zone-track"

    child_names = \
        ['track_zone']

    track_zone: track_zone_cls = track_zone_cls
    """
    track_zone child of zone_track.
    """
