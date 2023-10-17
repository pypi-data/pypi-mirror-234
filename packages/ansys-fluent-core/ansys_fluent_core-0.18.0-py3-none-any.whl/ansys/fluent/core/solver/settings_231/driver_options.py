#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .hardcopy_format import hardcopy_format as hardcopy_format_cls
from .hardcopy_options import hardcopy_options as hardcopy_options_cls
from .window_dump_cmd import window_dump_cmd as window_dump_cmd_cls
from .post_format import post_format as post_format_cls
from .current_driver import current_driver as current_driver_cls
class driver_options(Group):
    """
    'driver_options' child.
    """

    fluent_name = "driver-options"

    child_names = \
        ['hardcopy_format', 'hardcopy_options', 'window_dump_cmd',
         'post_format']

    hardcopy_format: hardcopy_format_cls = hardcopy_format_cls
    """
    hardcopy_format child of driver_options.
    """
    hardcopy_options: hardcopy_options_cls = hardcopy_options_cls
    """
    hardcopy_options child of driver_options.
    """
    window_dump_cmd: window_dump_cmd_cls = window_dump_cmd_cls
    """
    window_dump_cmd child of driver_options.
    """
    post_format: post_format_cls = post_format_cls
    """
    post_format child of driver_options.
    """
    command_names = \
        ['current_driver']

    current_driver: current_driver_cls = current_driver_cls
    """
    current_driver command of driver_options.
    """
