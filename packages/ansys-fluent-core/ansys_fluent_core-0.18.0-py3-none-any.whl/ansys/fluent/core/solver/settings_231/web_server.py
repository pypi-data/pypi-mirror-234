#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .start import start as start_cls
from .stop import stop as stop_cls
class web_server(Group):
    """
    'web_server' child.
    """

    fluent_name = "web-server"

    command_names = \
        ['start', 'stop']

    start: start_cls = start_cls
    """
    start command of web_server.
    """
    stop: stop_cls = stop_cls
    """
    stop command of web_server.
    """
