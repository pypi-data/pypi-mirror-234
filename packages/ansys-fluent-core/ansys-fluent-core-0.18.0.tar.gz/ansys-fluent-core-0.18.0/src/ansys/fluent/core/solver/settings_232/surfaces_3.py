#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .point_surface import point_surface as point_surface_cls
from .line_surface import line_surface as line_surface_cls
from .rake_surface import rake_surface as rake_surface_cls
from .iso_surface import iso_surface as iso_surface_cls
from .plane_surface import plane_surface as plane_surface_cls
class surfaces(Group):
    """
    'surfaces' child.
    """

    fluent_name = "surfaces"

    child_names = \
        ['point_surface', 'line_surface', 'rake_surface', 'iso_surface',
         'plane_surface']

    point_surface: point_surface_cls = point_surface_cls
    """
    point_surface child of surfaces.
    """
    line_surface: line_surface_cls = line_surface_cls
    """
    line_surface child of surfaces.
    """
    rake_surface: rake_surface_cls = rake_surface_cls
    """
    rake_surface child of surfaces.
    """
    iso_surface: iso_surface_cls = iso_surface_cls
    """
    iso_surface child of surfaces.
    """
    plane_surface: plane_surface_cls = plane_surface_cls
    """
    plane_surface child of surfaces.
    """
