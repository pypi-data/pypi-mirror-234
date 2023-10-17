#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .headlight_setting import headlight_setting as headlight_setting_cls
from .lights_on import lights_on as lights_on_cls
from .lighting_interpolation import lighting_interpolation as lighting_interpolation_cls
from .set_ambient_color import set_ambient_color as set_ambient_color_cls
from .set_light import set_light as set_light_cls
class lights(Group):
    """
    'lights' child.
    """

    fluent_name = "lights"

    child_names = \
        ['headlight_setting', 'lights_on', 'lighting_interpolation']

    headlight_setting: headlight_setting_cls = headlight_setting_cls
    """
    headlight_setting child of lights.
    """
    lights_on: lights_on_cls = lights_on_cls
    """
    lights_on child of lights.
    """
    lighting_interpolation: lighting_interpolation_cls = lighting_interpolation_cls
    """
    lighting_interpolation child of lights.
    """
    command_names = \
        ['set_ambient_color', 'set_light']

    set_ambient_color: set_ambient_color_cls = set_ambient_color_cls
    """
    set_ambient_color command of lights.
    """
    set_light: set_light_cls = set_light_cls
    """
    set_light command of lights.
    """
