#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .contour import contour as contour_cls
from .mesh_2 import mesh as mesh_cls
from .vector import vector as vector_cls
from .pathline import pathline as pathline_cls
from .particle_track import particle_track as particle_track_cls
from .lic import lic as lic_cls
from .olic import olic as olic_cls
from .contours import contours as contours_cls
from .particle_tracks import particle_tracks as particle_tracks_cls
from .colors import colors as colors_cls
from .lights import lights as lights_cls
from .picture import picture as picture_cls
from .views import views as views_cls
from .windows import windows as windows_cls
class graphics(Group, _ChildNamedObjectAccessorMixin):
    """
    'graphics' child.
    """

    fluent_name = "graphics"

    child_names = \
        ['contour', 'mesh', 'vector', 'pathline', 'particle_track', 'lic',
         'olic', 'contours', 'particle_tracks', 'colors', 'lights', 'picture',
         'views', 'windows']

    contour: contour_cls = contour_cls
    """
    contour child of graphics.
    """
    mesh: mesh_cls = mesh_cls
    """
    mesh child of graphics.
    """
    vector: vector_cls = vector_cls
    """
    vector child of graphics.
    """
    pathline: pathline_cls = pathline_cls
    """
    pathline child of graphics.
    """
    particle_track: particle_track_cls = particle_track_cls
    """
    particle_track child of graphics.
    """
    lic: lic_cls = lic_cls
    """
    lic child of graphics.
    """
    olic: olic_cls = olic_cls
    """
    olic child of graphics.
    """
    contours: contours_cls = contours_cls
    """
    contours child of graphics.
    """
    particle_tracks: particle_tracks_cls = particle_tracks_cls
    """
    particle_tracks child of graphics.
    """
    colors: colors_cls = colors_cls
    """
    colors child of graphics.
    """
    lights: lights_cls = lights_cls
    """
    lights child of graphics.
    """
    picture: picture_cls = picture_cls
    """
    picture child of graphics.
    """
    views: views_cls = views_cls
    """
    views child of graphics.
    """
    windows: windows_cls = windows_cls
    """
    windows child of graphics.
    """
