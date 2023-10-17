#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .center import center as center_cls
from .radius import radius as radius_cls
from .inside import inside as inside_cls
from .create_volume_surface import create_volume_surface as create_volume_surface_cls
class sphere(Group):
    """
    'sphere' child.
    """

    fluent_name = "sphere"

    child_names = \
        ['center', 'radius', 'inside', 'create_volume_surface']

    center: center_cls = center_cls
    """
    center child of sphere.
    """
    radius: radius_cls = radius_cls
    """
    radius child of sphere.
    """
    inside: inside_cls = inside_cls
    """
    inside child of sphere.
    """
    create_volume_surface: create_volume_surface_cls = create_volume_surface_cls
    """
    create_volume_surface child of sphere.
    """
