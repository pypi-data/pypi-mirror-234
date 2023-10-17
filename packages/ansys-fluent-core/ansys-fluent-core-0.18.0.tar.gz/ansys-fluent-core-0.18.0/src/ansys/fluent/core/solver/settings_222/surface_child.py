#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .custom_vector import custom_vector as custom_vector_cls
from .field import field as field_cls
from .surfaces import surfaces as surfaces_cls
from .geometry_1 import geometry as geometry_cls
from .physics import physics as physics_cls
from .retain_instantaneous_values import retain_instantaneous_values as retain_instantaneous_values_cls
from .report_type import report_type as report_type_cls
from .phase_25 import phase as phase_cls
from .average_over import average_over as average_over_cls
from .per_surface import per_surface as per_surface_cls
from .old_props import old_props as old_props_cls
from .surface_names import surface_names as surface_names_cls
from .surface_ids import surface_ids as surface_ids_cls
class surface_child(Group):
    """
    'child_object_type' of surface.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['custom_vector', 'field', 'surfaces', 'geometry', 'physics',
         'retain_instantaneous_values', 'report_type', 'phase',
         'average_over', 'per_surface', 'old_props', 'surface_names',
         'surface_ids']

    custom_vector: custom_vector_cls = custom_vector_cls
    """
    custom_vector child of surface_child.
    """
    field: field_cls = field_cls
    """
    field child of surface_child.
    """
    surfaces: surfaces_cls = surfaces_cls
    """
    surfaces child of surface_child.
    """
    geometry: geometry_cls = geometry_cls
    """
    geometry child of surface_child.
    """
    physics: physics_cls = physics_cls
    """
    physics child of surface_child.
    """
    retain_instantaneous_values: retain_instantaneous_values_cls = retain_instantaneous_values_cls
    """
    retain_instantaneous_values child of surface_child.
    """
    report_type: report_type_cls = report_type_cls
    """
    report_type child of surface_child.
    """
    phase: phase_cls = phase_cls
    """
    phase child of surface_child.
    """
    average_over: average_over_cls = average_over_cls
    """
    average_over child of surface_child.
    """
    per_surface: per_surface_cls = per_surface_cls
    """
    per_surface child of surface_child.
    """
    old_props: old_props_cls = old_props_cls
    """
    old_props child of surface_child.
    """
    surface_names: surface_names_cls = surface_names_cls
    """
    surface_names child of surface_child.
    """
    surface_ids: surface_ids_cls = surface_ids_cls
    """
    surface_ids child of surface_child.
    """
