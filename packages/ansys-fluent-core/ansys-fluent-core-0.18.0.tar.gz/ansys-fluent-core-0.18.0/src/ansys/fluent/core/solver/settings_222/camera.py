#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .dolly import dolly as dolly_cls
from .field_1 import field as field_cls
from .orbit import orbit as orbit_cls
from .pan import pan as pan_cls
from .position_1 import position as position_cls
from .projection import projection as projection_cls
from .roll import roll as roll_cls
from .target import target as target_cls
from .up_vector import up_vector as up_vector_cls
from .zoom import zoom as zoom_cls
class camera(Group):
    """
    'camera' child.
    """

    fluent_name = "camera"

    command_names = \
        ['dolly', 'field', 'orbit', 'pan', 'position', 'projection', 'roll',
         'target', 'up_vector', 'zoom']

    dolly: dolly_cls = dolly_cls
    """
    dolly command of camera.
    """
    field: field_cls = field_cls
    """
    field command of camera.
    """
    orbit: orbit_cls = orbit_cls
    """
    orbit command of camera.
    """
    pan: pan_cls = pan_cls
    """
    pan command of camera.
    """
    position: position_cls = position_cls
    """
    position command of camera.
    """
    projection: projection_cls = projection_cls
    """
    projection command of camera.
    """
    roll: roll_cls = roll_cls
    """
    roll command of camera.
    """
    target: target_cls = target_cls
    """
    target command of camera.
    """
    up_vector: up_vector_cls = up_vector_cls
    """
    up_vector command of camera.
    """
    zoom: zoom_cls = zoom_cls
    """
    zoom command of camera.
    """
