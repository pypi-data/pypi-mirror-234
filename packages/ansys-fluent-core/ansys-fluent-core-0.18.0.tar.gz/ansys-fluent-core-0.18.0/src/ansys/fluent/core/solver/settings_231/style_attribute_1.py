#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .style import style as style_cls
from .line_width import line_width as line_width_cls
from .arrow_space import arrow_space as arrow_space_cls
from .arrow_scale import arrow_scale as arrow_scale_cls
from .marker_size import marker_size as marker_size_cls
from .sphere_size import sphere_size as sphere_size_cls
from .sphere_lod import sphere_lod as sphere_lod_cls
from .radius import radius as radius_cls
from .ribbon_settings import ribbon_settings as ribbon_settings_cls
from .sphere_settings import sphere_settings as sphere_settings_cls
class style_attribute(Group):
    """
    'style_attribute' child.
    """

    fluent_name = "style-attribute"

    child_names = \
        ['style', 'line_width', 'arrow_space', 'arrow_scale', 'marker_size',
         'sphere_size', 'sphere_lod', 'radius', 'ribbon_settings',
         'sphere_settings']

    style: style_cls = style_cls
    """
    style child of style_attribute.
    """
    line_width: line_width_cls = line_width_cls
    """
    line_width child of style_attribute.
    """
    arrow_space: arrow_space_cls = arrow_space_cls
    """
    arrow_space child of style_attribute.
    """
    arrow_scale: arrow_scale_cls = arrow_scale_cls
    """
    arrow_scale child of style_attribute.
    """
    marker_size: marker_size_cls = marker_size_cls
    """
    marker_size child of style_attribute.
    """
    sphere_size: sphere_size_cls = sphere_size_cls
    """
    sphere_size child of style_attribute.
    """
    sphere_lod: sphere_lod_cls = sphere_lod_cls
    """
    sphere_lod child of style_attribute.
    """
    radius: radius_cls = radius_cls
    """
    radius child of style_attribute.
    """
    ribbon_settings: ribbon_settings_cls = ribbon_settings_cls
    """
    ribbon_settings child of style_attribute.
    """
    sphere_settings: sphere_settings_cls = sphere_settings_cls
    """
    sphere_settings child of style_attribute.
    """
