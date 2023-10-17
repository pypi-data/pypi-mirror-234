#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .methods_2 import methods as methods_cls
from .x import x as x_cls
from .y import y as y_cls
from .z import z as z_cls
from .point_vector import point_vector as point_vector_cls
from .point_normal import point_normal as point_normal_cls
from .compute_from_view_plane import compute_from_view_plane as compute_from_view_plane_cls
from .surface_aligned_normal import surface_aligned_normal as surface_aligned_normal_cls
from .p0_1 import p0 as p0_cls
from .p1 import p1 as p1_cls
from .p2 import p2 as p2_cls
from .bounded import bounded as bounded_cls
from .sample_point import sample_point as sample_point_cls
from .edges_2 import edges as edges_cls
class plane_surface_child(Group):
    """
    'child_object_type' of plane_surface.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['methods', 'x', 'y', 'z', 'point_vector', 'point_normal',
         'compute_from_view_plane', 'surface_aligned_normal', 'p0', 'p1',
         'p2', 'bounded', 'sample_point', 'edges']

    methods: methods_cls = methods_cls
    """
    methods child of plane_surface_child.
    """
    x: x_cls = x_cls
    """
    x child of plane_surface_child.
    """
    y: y_cls = y_cls
    """
    y child of plane_surface_child.
    """
    z: z_cls = z_cls
    """
    z child of plane_surface_child.
    """
    point_vector: point_vector_cls = point_vector_cls
    """
    point_vector child of plane_surface_child.
    """
    point_normal: point_normal_cls = point_normal_cls
    """
    point_normal child of plane_surface_child.
    """
    compute_from_view_plane: compute_from_view_plane_cls = compute_from_view_plane_cls
    """
    compute_from_view_plane child of plane_surface_child.
    """
    surface_aligned_normal: surface_aligned_normal_cls = surface_aligned_normal_cls
    """
    surface_aligned_normal child of plane_surface_child.
    """
    p0: p0_cls = p0_cls
    """
    p0 child of plane_surface_child.
    """
    p1: p1_cls = p1_cls
    """
    p1 child of plane_surface_child.
    """
    p2: p2_cls = p2_cls
    """
    p2 child of plane_surface_child.
    """
    bounded: bounded_cls = bounded_cls
    """
    bounded child of plane_surface_child.
    """
    sample_point: sample_point_cls = sample_point_cls
    """
    sample_point child of plane_surface_child.
    """
    edges: edges_cls = edges_cls
    """
    edges child of plane_surface_child.
    """
