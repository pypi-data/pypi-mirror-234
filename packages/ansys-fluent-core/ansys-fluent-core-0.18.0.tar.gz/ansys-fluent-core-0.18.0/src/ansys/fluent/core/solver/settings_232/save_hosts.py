#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .host_file import host_file as host_file_cls
class save_hosts(Command):
    """
    Write a hosts file.
    
    Parameters
    ----------
        host_file : str
            'host_file' child.
    
    """

    fluent_name = "save-hosts"

    argument_names = \
        ['host_file']

    host_file: host_file_cls = host_file_cls
    """
    host_file argument of save_hosts.
    """
