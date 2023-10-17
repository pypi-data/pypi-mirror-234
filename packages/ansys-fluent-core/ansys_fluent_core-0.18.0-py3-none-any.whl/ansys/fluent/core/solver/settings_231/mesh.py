#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .adapt import adapt as adapt_cls
from .check_before_solve import check_before_solve as check_before_solve_cls
from .check_verbosity import check_verbosity as check_verbosity_cls
from .enhanced_orthogonal_quality import enhanced_orthogonal_quality as enhanced_orthogonal_quality_cls
from .matching_tolerance import matching_tolerance as matching_tolerance_cls
from .show_periodic_shadow_zones import show_periodic_shadow_zones as show_periodic_shadow_zones_cls
from .reorder import reorder as reorder_cls
from .repair_improve import repair_improve as repair_improve_cls
from .surface_mesh import surface_mesh as surface_mesh_cls
from .polyhedra import polyhedra as polyhedra_cls
from .adjacency import adjacency as adjacency_cls
from .check import check as check_cls
from .memory_usage import memory_usage as memory_usage_cls
from .mesh_info import mesh_info as mesh_info_cls
from .quality import quality as quality_cls
from .rotate import rotate as rotate_cls
from .scale import scale as scale_cls
from .size_info import size_info as size_info_cls
from .redistribute_boundary_layer import redistribute_boundary_layer as redistribute_boundary_layer_cls
from .swap_mesh_faces import swap_mesh_faces as swap_mesh_faces_cls
from .smooth_mesh import smooth_mesh as smooth_mesh_cls
from .replace import replace as replace_cls
from .translate import translate as translate_cls
class mesh(Group):
    """
    'mesh' child.
    """

    fluent_name = "mesh"

    child_names = \
        ['adapt', 'check_before_solve', 'check_verbosity',
         'enhanced_orthogonal_quality', 'matching_tolerance',
         'show_periodic_shadow_zones', 'reorder', 'repair_improve',
         'surface_mesh', 'polyhedra']

    adapt: adapt_cls = adapt_cls
    """
    adapt child of mesh.
    """
    check_before_solve: check_before_solve_cls = check_before_solve_cls
    """
    check_before_solve child of mesh.
    """
    check_verbosity: check_verbosity_cls = check_verbosity_cls
    """
    check_verbosity child of mesh.
    """
    enhanced_orthogonal_quality: enhanced_orthogonal_quality_cls = enhanced_orthogonal_quality_cls
    """
    enhanced_orthogonal_quality child of mesh.
    """
    matching_tolerance: matching_tolerance_cls = matching_tolerance_cls
    """
    matching_tolerance child of mesh.
    """
    show_periodic_shadow_zones: show_periodic_shadow_zones_cls = show_periodic_shadow_zones_cls
    """
    show_periodic_shadow_zones child of mesh.
    """
    reorder: reorder_cls = reorder_cls
    """
    reorder child of mesh.
    """
    repair_improve: repair_improve_cls = repair_improve_cls
    """
    repair_improve child of mesh.
    """
    surface_mesh: surface_mesh_cls = surface_mesh_cls
    """
    surface_mesh child of mesh.
    """
    polyhedra: polyhedra_cls = polyhedra_cls
    """
    polyhedra child of mesh.
    """
    command_names = \
        ['adjacency', 'check', 'memory_usage', 'mesh_info', 'quality',
         'rotate', 'scale', 'size_info', 'redistribute_boundary_layer',
         'swap_mesh_faces', 'smooth_mesh', 'replace', 'translate']

    adjacency: adjacency_cls = adjacency_cls
    """
    adjacency command of mesh.
    """
    check: check_cls = check_cls
    """
    check command of mesh.
    """
    memory_usage: memory_usage_cls = memory_usage_cls
    """
    memory_usage command of mesh.
    """
    mesh_info: mesh_info_cls = mesh_info_cls
    """
    mesh_info command of mesh.
    """
    quality: quality_cls = quality_cls
    """
    quality command of mesh.
    """
    rotate: rotate_cls = rotate_cls
    """
    rotate command of mesh.
    """
    scale: scale_cls = scale_cls
    """
    scale command of mesh.
    """
    size_info: size_info_cls = size_info_cls
    """
    size_info command of mesh.
    """
    redistribute_boundary_layer: redistribute_boundary_layer_cls = redistribute_boundary_layer_cls
    """
    redistribute_boundary_layer command of mesh.
    """
    swap_mesh_faces: swap_mesh_faces_cls = swap_mesh_faces_cls
    """
    swap_mesh_faces command of mesh.
    """
    smooth_mesh: smooth_mesh_cls = smooth_mesh_cls
    """
    smooth_mesh command of mesh.
    """
    replace: replace_cls = replace_cls
    """
    replace command of mesh.
    """
    translate: translate_cls = translate_cls
    """
    translate command of mesh.
    """
