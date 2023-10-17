#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .mesh_1 import mesh as mesh_cls
from .contour import contour as contour_cls
from .vector import vector as vector_cls
from .pathlines import pathlines as pathlines_cls
from .particle_tracks import particle_tracks as particle_tracks_cls
from .lic import lic as lic_cls
from .views import views as views_cls
class graphics(Group):
    """
    'graphics' child.
    """

    fluent_name = "graphics"

    child_names = \
        ['mesh', 'contour', 'vector', 'pathlines', 'particle_tracks', 'lic',
         'views']

    mesh: mesh_cls = mesh_cls
    """
    mesh child of graphics.
    """
    contour: contour_cls = contour_cls
    """
    contour child of graphics.
    """
    vector: vector_cls = vector_cls
    """
    vector child of graphics.
    """
    pathlines: pathlines_cls = pathlines_cls
    """
    pathlines child of graphics.
    """
    particle_tracks: particle_tracks_cls = particle_tracks_cls
    """
    particle_tracks child of graphics.
    """
    lic: lic_cls = lic_cls
    """
    lic child of graphics.
    """
    views: views_cls = views_cls
    """
    views child of graphics.
    """
