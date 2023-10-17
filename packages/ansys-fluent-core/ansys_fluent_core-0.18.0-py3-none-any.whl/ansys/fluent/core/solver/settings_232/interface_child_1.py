#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .interface_names import interface_names as interface_names_cls
from .zone_names import zone_names as zone_names_cls
from .zone1 import zone1 as zone1_cls
from .zone2 import zone2 as zone2_cls
from .new_zones import new_zones as new_zones_cls
from .mapped import mapped as mapped_cls
from .enable_local_mapped_tolerance import enable_local_mapped_tolerance as enable_local_mapped_tolerance_cls
from .use_local_edge_length_factor import use_local_edge_length_factor as use_local_edge_length_factor_cls
from .local_relative_mapped_tolerance import local_relative_mapped_tolerance as local_relative_mapped_tolerance_cls
from .local_absolute_mapped_tolerance import local_absolute_mapped_tolerance as local_absolute_mapped_tolerance_cls
from .periodic_1 import periodic as periodic_cls
from .turbo import turbo as turbo_cls
from .pitch_change_types import pitch_change_types as pitch_change_types_cls
from .mixing_plane import mixing_plane as mixing_plane_cls
from .turbo_non_overlap import turbo_non_overlap as turbo_non_overlap_cls
from .coupled import coupled as coupled_cls
from .matching import matching as matching_cls
from .static import static as static_cls
from .ignore_diff import ignore_diff as ignore_diff_cls
class interface_child(Group):
    """
    'child_object_type' of interface.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['interface_names', 'zone_names', 'zone1', 'zone2', 'new_zones',
         'mapped', 'enable_local_mapped_tolerance',
         'use_local_edge_length_factor', 'local_relative_mapped_tolerance',
         'local_absolute_mapped_tolerance', 'periodic', 'turbo',
         'pitch_change_types', 'mixing_plane', 'turbo_non_overlap', 'coupled',
         'matching', 'static', 'ignore_diff']

    interface_names: interface_names_cls = interface_names_cls
    """
    interface_names child of interface_child.
    """
    zone_names: zone_names_cls = zone_names_cls
    """
    zone_names child of interface_child.
    """
    zone1: zone1_cls = zone1_cls
    """
    zone1 child of interface_child.
    """
    zone2: zone2_cls = zone2_cls
    """
    zone2 child of interface_child.
    """
    new_zones: new_zones_cls = new_zones_cls
    """
    new_zones child of interface_child.
    """
    mapped: mapped_cls = mapped_cls
    """
    mapped child of interface_child.
    """
    enable_local_mapped_tolerance: enable_local_mapped_tolerance_cls = enable_local_mapped_tolerance_cls
    """
    enable_local_mapped_tolerance child of interface_child.
    """
    use_local_edge_length_factor: use_local_edge_length_factor_cls = use_local_edge_length_factor_cls
    """
    use_local_edge_length_factor child of interface_child.
    """
    local_relative_mapped_tolerance: local_relative_mapped_tolerance_cls = local_relative_mapped_tolerance_cls
    """
    local_relative_mapped_tolerance child of interface_child.
    """
    local_absolute_mapped_tolerance: local_absolute_mapped_tolerance_cls = local_absolute_mapped_tolerance_cls
    """
    local_absolute_mapped_tolerance child of interface_child.
    """
    periodic: periodic_cls = periodic_cls
    """
    periodic child of interface_child.
    """
    turbo: turbo_cls = turbo_cls
    """
    turbo child of interface_child.
    """
    pitch_change_types: pitch_change_types_cls = pitch_change_types_cls
    """
    pitch_change_types child of interface_child.
    """
    mixing_plane: mixing_plane_cls = mixing_plane_cls
    """
    mixing_plane child of interface_child.
    """
    turbo_non_overlap: turbo_non_overlap_cls = turbo_non_overlap_cls
    """
    turbo_non_overlap child of interface_child.
    """
    coupled: coupled_cls = coupled_cls
    """
    coupled child of interface_child.
    """
    matching: matching_cls = matching_cls
    """
    matching child of interface_child.
    """
    static: static_cls = static_cls
    """
    static child of interface_child.
    """
    ignore_diff: ignore_diff_cls = ignore_diff_cls
    """
    ignore_diff child of interface_child.
    """
