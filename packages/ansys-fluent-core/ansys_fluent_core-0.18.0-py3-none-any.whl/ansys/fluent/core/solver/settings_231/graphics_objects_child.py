#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .name_1 import name as name_cls
from .transparency import transparency as transparency_cls
from .colormap_position import colormap_position as colormap_position_cls
from .colormap_left import colormap_left as colormap_left_cls
from .colormap_bottom import colormap_bottom as colormap_bottom_cls
from .colormap_width import colormap_width as colormap_width_cls
from .colormap_height import colormap_height as colormap_height_cls
class graphics_objects_child(Group):
    """
    'child_object_type' of graphics_objects.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'transparency', 'colormap_position', 'colormap_left',
         'colormap_bottom', 'colormap_width', 'colormap_height']

    name: name_cls = name_cls
    """
    name child of graphics_objects_child.
    """
    transparency: transparency_cls = transparency_cls
    """
    transparency child of graphics_objects_child.
    """
    colormap_position: colormap_position_cls = colormap_position_cls
    """
    colormap_position child of graphics_objects_child.
    """
    colormap_left: colormap_left_cls = colormap_left_cls
    """
    colormap_left child of graphics_objects_child.
    """
    colormap_bottom: colormap_bottom_cls = colormap_bottom_cls
    """
    colormap_bottom child of graphics_objects_child.
    """
    colormap_width: colormap_width_cls = colormap_width_cls
    """
    colormap_width child of graphics_objects_child.
    """
    colormap_height: colormap_height_cls = colormap_height_cls
    """
    colormap_height child of graphics_objects_child.
    """
