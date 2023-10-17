#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .quality_1 import quality as quality_cls
from .denoiser import denoiser as denoiser_cls
from .thread_count import thread_count as thread_count_cls
from .max_rendering_timeout import max_rendering_timeout as max_rendering_timeout_cls
class rendering(Group):
    """
    Enter the menu for rendering options.
    """

    fluent_name = "rendering"

    child_names = \
        ['quality', 'denoiser', 'thread_count', 'max_rendering_timeout']

    quality: quality_cls = quality_cls
    """
    quality child of rendering.
    """
    denoiser: denoiser_cls = denoiser_cls
    """
    denoiser child of rendering.
    """
    thread_count: thread_count_cls = thread_count_cls
    """
    thread_count child of rendering.
    """
    max_rendering_timeout: max_rendering_timeout_cls = max_rendering_timeout_cls
    """
    max_rendering_timeout child of rendering.
    """
