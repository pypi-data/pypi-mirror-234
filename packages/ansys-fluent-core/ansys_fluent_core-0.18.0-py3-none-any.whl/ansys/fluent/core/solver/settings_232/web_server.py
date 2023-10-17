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
from .print_server_info import print_server_info as print_server_info_cls
from .get_server_info import get_server_info as get_server_info_cls
class web_server(Group):
    """
    REST and WebSocket based web server.
    """

    fluent_name = "web-server"

    command_names = \
        ['start', 'stop', 'print_server_info']

    start: start_cls = start_cls
    """
    start command of web_server.
    """
    stop: stop_cls = stop_cls
    """
    stop command of web_server.
    """
    print_server_info: print_server_info_cls = print_server_info_cls
    """
    print_server_info command of web_server.
    """
    query_names = \
        ['get_server_info']

    get_server_info: get_server_info_cls = get_server_info_cls
    """
    get_server_info query of web_server.
    """
