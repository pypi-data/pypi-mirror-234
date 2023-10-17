#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .hide_environment_keep_effects import hide_environment_keep_effects as hide_environment_keep_effects_cls
from .environment_image import environment_image as environment_image_cls
from .latitude_1 import latitude as latitude_cls
from .longitude_1 import longitude as longitude_cls
from .view_zoom import view_zoom as view_zoom_cls
from .show_backplate import show_backplate as show_backplate_cls
from .backplate_color import backplate_color as backplate_color_cls
from .backplate_image import backplate_image as backplate_image_cls
class background(Group):
    """
    Enter the menu for background options.
    """

    fluent_name = "background"

    child_names = \
        ['hide_environment_keep_effects', 'environment_image', 'latitude',
         'longitude', 'view_zoom', 'show_backplate', 'backplate_color',
         'backplate_image']

    hide_environment_keep_effects: hide_environment_keep_effects_cls = hide_environment_keep_effects_cls
    """
    hide_environment_keep_effects child of background.
    """
    environment_image: environment_image_cls = environment_image_cls
    """
    environment_image child of background.
    """
    latitude: latitude_cls = latitude_cls
    """
    latitude child of background.
    """
    longitude: longitude_cls = longitude_cls
    """
    longitude child of background.
    """
    view_zoom: view_zoom_cls = view_zoom_cls
    """
    view_zoom child of background.
    """
    show_backplate: show_backplate_cls = show_backplate_cls
    """
    show_backplate child of background.
    """
    backplate_color: backplate_color_cls = backplate_color_cls
    """
    backplate_color child of background.
    """
    backplate_image: backplate_image_cls = backplate_image_cls
    """
    backplate_image child of background.
    """
