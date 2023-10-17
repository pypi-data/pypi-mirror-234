#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .name_1 import name as name_cls
from .p0 import p0 as p0_cls
from .p1 import p1 as p1_cls
from .number_of_points import number_of_points as number_of_points_cls
class rake_surface_child(Group):
    """
    'child_object_type' of rake_surface.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'p0', 'p1', 'number_of_points']

    name: name_cls = name_cls
    """
    name child of rake_surface_child.
    """
    p0: p0_cls = p0_cls
    """
    p0 child of rake_surface_child.
    """
    p1: p1_cls = p1_cls
    """
    p1 child of rake_surface_child.
    """
    number_of_points: number_of_points_cls = number_of_points_cls
    """
    number_of_points child of rake_surface_child.
    """
