#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .option_2 import option as option_cls
from .volume_magnitude import volume_magnitude as volume_magnitude_cls
from .volume_change import volume_change as volume_change_cls
class volume(Group):
    """
    'volume' child.
    """

    fluent_name = "volume"

    child_names = \
        ['option', 'volume_magnitude', 'volume_change']

    option: option_cls = option_cls
    """
    option child of volume.
    """
    volume_magnitude: volume_magnitude_cls = volume_magnitude_cls
    """
    volume_magnitude child of volume.
    """
    volume_change: volume_change_cls = volume_change_cls
    """
    volume_change child of volume.
    """
