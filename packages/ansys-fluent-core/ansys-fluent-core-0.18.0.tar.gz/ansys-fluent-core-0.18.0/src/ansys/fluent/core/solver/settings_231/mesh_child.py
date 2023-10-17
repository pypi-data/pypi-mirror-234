#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .zone_ids import zone_ids as zone_ids_cls
from .retain_instantaneous_values import retain_instantaneous_values as retain_instantaneous_values_cls
from .old_props import old_props as old_props_cls
from .zone_names import zone_names as zone_names_cls
from .zone_list import zone_list as zone_list_cls
from .average_over import average_over as average_over_cls
from .per_zone import per_zone as per_zone_cls
class mesh_child(Group):
    """
    'child_object_type' of mesh.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['zone_ids', 'retain_instantaneous_values', 'old_props', 'zone_names',
         'zone_list', 'average_over', 'per_zone']

    zone_ids: zone_ids_cls = zone_ids_cls
    """
    zone_ids child of mesh_child.
    """
    retain_instantaneous_values: retain_instantaneous_values_cls = retain_instantaneous_values_cls
    """
    retain_instantaneous_values child of mesh_child.
    """
    old_props: old_props_cls = old_props_cls
    """
    old_props child of mesh_child.
    """
    zone_names: zone_names_cls = zone_names_cls
    """
    zone_names child of mesh_child.
    """
    zone_list: zone_list_cls = zone_list_cls
    """
    zone_list child of mesh_child.
    """
    average_over: average_over_cls = average_over_cls
    """
    average_over child of mesh_child.
    """
    per_zone: per_zone_cls = per_zone_cls
    """
    per_zone child of mesh_child.
    """
