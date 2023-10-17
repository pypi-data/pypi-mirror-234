#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .zone1_1 import zone1 as zone1_cls
from .zone2_1 import zone2 as zone2_cls
from .pitch_change_types import pitch_change_types as pitch_change_types_cls
from .mixing_plane import mixing_plane as mixing_plane_cls
from .turbo_non_overlap import turbo_non_overlap as turbo_non_overlap_cls
class turbo_interface_child(Group):
    """
    'child_object_type' of turbo_interface.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['zone1', 'zone2', 'pitch_change_types', 'mixing_plane',
         'turbo_non_overlap']

    zone1: zone1_cls = zone1_cls
    """
    zone1 child of turbo_interface_child.
    """
    zone2: zone2_cls = zone2_cls
    """
    zone2 child of turbo_interface_child.
    """
    pitch_change_types: pitch_change_types_cls = pitch_change_types_cls
    """
    pitch_change_types child of turbo_interface_child.
    """
    mixing_plane: mixing_plane_cls = mixing_plane_cls
    """
    mixing_plane child of turbo_interface_child.
    """
    turbo_non_overlap: turbo_non_overlap_cls = turbo_non_overlap_cls
    """
    turbo_non_overlap child of turbo_interface_child.
    """
