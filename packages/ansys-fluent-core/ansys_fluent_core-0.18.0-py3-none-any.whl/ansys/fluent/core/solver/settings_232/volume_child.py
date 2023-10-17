#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .name_1 import name as name_cls
from .report_type import report_type as report_type_cls
from .geometry_4 import geometry as geometry_cls
from .physics_1 import physics as physics_cls
from .field import field as field_cls
from .retain_instantaneous_values import retain_instantaneous_values as retain_instantaneous_values_cls
from .phase_25 import phase as phase_cls
from .average_over import average_over as average_over_cls
from .per_zone import per_zone as per_zone_cls
from .old_props import old_props as old_props_cls
from .zone_names_1 import zone_names as zone_names_cls
from .expr_list import expr_list as expr_list_cls
from .zone_list import zone_list as zone_list_cls
class volume_child(Group):
    """
    'child_object_type' of volume.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'report_type', 'geometry', 'physics', 'field',
         'retain_instantaneous_values', 'phase', 'average_over', 'per_zone',
         'old_props', 'zone_names', 'expr_list', 'zone_list']

    name: name_cls = name_cls
    """
    name child of volume_child.
    """
    report_type: report_type_cls = report_type_cls
    """
    report_type child of volume_child.
    """
    geometry: geometry_cls = geometry_cls
    """
    geometry child of volume_child.
    """
    physics: physics_cls = physics_cls
    """
    physics child of volume_child.
    """
    field: field_cls = field_cls
    """
    field child of volume_child.
    """
    retain_instantaneous_values: retain_instantaneous_values_cls = retain_instantaneous_values_cls
    """
    retain_instantaneous_values child of volume_child.
    """
    phase: phase_cls = phase_cls
    """
    phase child of volume_child.
    """
    average_over: average_over_cls = average_over_cls
    """
    average_over child of volume_child.
    """
    per_zone: per_zone_cls = per_zone_cls
    """
    per_zone child of volume_child.
    """
    old_props: old_props_cls = old_props_cls
    """
    old_props child of volume_child.
    """
    zone_names: zone_names_cls = zone_names_cls
    """
    zone_names child of volume_child.
    """
    expr_list: expr_list_cls = expr_list_cls
    """
    expr_list child of volume_child.
    """
    zone_list: zone_list_cls = zone_list_cls
    """
    zone_list child of volume_child.
    """
