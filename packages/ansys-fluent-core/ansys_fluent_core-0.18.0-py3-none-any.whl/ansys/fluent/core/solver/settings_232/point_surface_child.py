#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .name_1 import name as name_cls
from .reference_frame import reference_frame as reference_frame_cls
from .point import point as point_cls
from .snap_method import snap_method as snap_method_cls
class point_surface_child(Group):
    """
    'child_object_type' of point_surface.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'reference_frame', 'point', 'snap_method']

    name: name_cls = name_cls
    """
    name child of point_surface_child.
    """
    reference_frame: reference_frame_cls = reference_frame_cls
    """
    reference_frame child of point_surface_child.
    """
    point: point_cls = point_cls
    """
    point child of point_surface_child.
    """
    snap_method: snap_method_cls = snap_method_cls
    """
    snap_method child of point_surface_child.
    """
