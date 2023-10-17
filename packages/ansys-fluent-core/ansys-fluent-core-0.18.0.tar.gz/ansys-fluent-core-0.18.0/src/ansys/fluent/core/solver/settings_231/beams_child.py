#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .ap_face_zone import ap_face_zone as ap_face_zone_cls
from .beam_length import beam_length as beam_length_cls
from .ray_points_count import ray_points_count as ray_points_count_cls
from .beam_vector import beam_vector as beam_vector_cls
class beams_child(Group):
    """
    'child_object_type' of beams.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['ap_face_zone', 'beam_length', 'ray_points_count', 'beam_vector']

    ap_face_zone: ap_face_zone_cls = ap_face_zone_cls
    """
    ap_face_zone child of beams_child.
    """
    beam_length: beam_length_cls = beam_length_cls
    """
    beam_length child of beams_child.
    """
    ray_points_count: ray_points_count_cls = ray_points_count_cls
    """
    ray_points_count child of beams_child.
    """
    beam_vector: beam_vector_cls = beam_vector_cls
    """
    beam_vector child of beams_child.
    """
