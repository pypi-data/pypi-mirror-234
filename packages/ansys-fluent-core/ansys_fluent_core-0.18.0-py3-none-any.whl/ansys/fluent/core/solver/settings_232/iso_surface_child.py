#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .name_1 import name as name_cls
from .field import field as field_cls
from .surface_2 import surface as surface_cls
from .zone_1 import zone as zone_cls
from .min import min as min_cls
from .max import max as max_cls
from .iso_value import iso_value as iso_value_cls
class iso_surface_child(Group):
    """
    'child_object_type' of iso_surface.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'field', 'surface', 'zone', 'min', 'max', 'iso_value']

    name: name_cls = name_cls
    """
    name child of iso_surface_child.
    """
    field: field_cls = field_cls
    """
    field child of iso_surface_child.
    """
    surface: surface_cls = surface_cls
    """
    surface child of iso_surface_child.
    """
    zone: zone_cls = zone_cls
    """
    zone child of iso_surface_child.
    """
    min: min_cls = min_cls
    """
    min child of iso_surface_child.
    """
    max: max_cls = max_cls
    """
    max child of iso_surface_child.
    """
    iso_value: iso_value_cls = iso_value_cls
    """
    iso_value child of iso_surface_child.
    """
