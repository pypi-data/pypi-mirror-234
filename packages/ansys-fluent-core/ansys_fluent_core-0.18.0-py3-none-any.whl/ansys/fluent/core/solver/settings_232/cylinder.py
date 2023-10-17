#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .axis_begin import axis_begin as axis_begin_cls
from .axis_end import axis_end as axis_end_cls
from .radius import radius as radius_cls
from .inside import inside as inside_cls
from .create_volume_surface import create_volume_surface as create_volume_surface_cls
class cylinder(Group):
    """
    'cylinder' child.
    """

    fluent_name = "cylinder"

    child_names = \
        ['axis_begin', 'axis_end', 'radius', 'inside',
         'create_volume_surface']

    axis_begin: axis_begin_cls = axis_begin_cls
    """
    axis_begin child of cylinder.
    """
    axis_end: axis_end_cls = axis_end_cls
    """
    axis_end child of cylinder.
    """
    radius: radius_cls = radius_cls
    """
    radius child of cylinder.
    """
    inside: inside_cls = inside_cls
    """
    inside child of cylinder.
    """
    create_volume_surface: create_volume_surface_cls = create_volume_surface_cls
    """
    create_volume_surface child of cylinder.
    """
