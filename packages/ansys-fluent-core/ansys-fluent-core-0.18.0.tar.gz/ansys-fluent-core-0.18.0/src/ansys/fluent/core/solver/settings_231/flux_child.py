#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .report_type import report_type as report_type_cls
from .geometry_3 import geometry as geometry_cls
from .physics import physics as physics_cls
from .retain_instantaneous_values import retain_instantaneous_values as retain_instantaneous_values_cls
from .phase_25 import phase as phase_cls
from .average_over import average_over as average_over_cls
from .per_zone import per_zone as per_zone_cls
from .old_props import old_props as old_props_cls
from .zone_names import zone_names as zone_names_cls
from .zone_ids import zone_ids as zone_ids_cls
class flux_child(Group):
    """
    'child_object_type' of flux.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['report_type', 'geometry', 'physics', 'retain_instantaneous_values',
         'phase', 'average_over', 'per_zone', 'old_props', 'zone_names',
         'zone_ids']

    report_type: report_type_cls = report_type_cls
    """
    report_type child of flux_child.
    """
    geometry: geometry_cls = geometry_cls
    """
    geometry child of flux_child.
    """
    physics: physics_cls = physics_cls
    """
    physics child of flux_child.
    """
    retain_instantaneous_values: retain_instantaneous_values_cls = retain_instantaneous_values_cls
    """
    retain_instantaneous_values child of flux_child.
    """
    phase: phase_cls = phase_cls
    """
    phase child of flux_child.
    """
    average_over: average_over_cls = average_over_cls
    """
    average_over child of flux_child.
    """
    per_zone: per_zone_cls = per_zone_cls
    """
    per_zone child of flux_child.
    """
    old_props: old_props_cls = old_props_cls
    """
    old_props child of flux_child.
    """
    zone_names: zone_names_cls = zone_names_cls
    """
    zone_names child of flux_child.
    """
    zone_ids: zone_ids_cls = zone_ids_cls
    """
    zone_ids child of flux_child.
    """
