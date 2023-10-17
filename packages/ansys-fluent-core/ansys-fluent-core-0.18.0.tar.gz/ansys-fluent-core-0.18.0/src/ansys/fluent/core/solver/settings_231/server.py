#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .web_server import web_server as web_server_cls
class server(Group):
    """
    'server' child.
    """

    fluent_name = "server"

    child_names = \
        ['web_server']

    web_server: web_server_cls = web_server_cls
    """
    web_server child of server.
    """
