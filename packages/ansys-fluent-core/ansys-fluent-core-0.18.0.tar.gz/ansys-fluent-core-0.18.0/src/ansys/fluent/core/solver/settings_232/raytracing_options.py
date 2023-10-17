#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .background_2 import background as background_cls
from .rendering import rendering as rendering_cls
from .display_live_preview import display_live_preview as display_live_preview_cls
class raytracing_options(Group):
    """
    'raytracing_options' child.
    """

    fluent_name = "raytracing-options"

    child_names = \
        ['background', 'rendering']

    background: background_cls = background_cls
    """
    background child of raytracing_options.
    """
    rendering: rendering_cls = rendering_cls
    """
    rendering child of raytracing_options.
    """
    command_names = \
        ['display_live_preview']

    display_live_preview: display_live_preview_cls = display_live_preview_cls
    """
    display_live_preview command of raytracing_options.
    """
