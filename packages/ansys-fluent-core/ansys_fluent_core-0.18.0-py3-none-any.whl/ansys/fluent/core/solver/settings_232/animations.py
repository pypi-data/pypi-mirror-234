#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .playback import playback as playback_cls
class animations(Group):
    """
    'animations' child.
    """

    fluent_name = "animations"

    child_names = \
        ['playback']

    playback: playback_cls = playback_cls
    """
    playback child of animations.
    """
