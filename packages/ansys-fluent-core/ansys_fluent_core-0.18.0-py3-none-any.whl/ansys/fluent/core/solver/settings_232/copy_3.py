#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .command_name import command_name as command_name_cls
class copy(Command):
    """
    Copy an execute-command.
    
    Parameters
    ----------
        command_name : str
            'command_name' child.
    
    """

    fluent_name = "copy"

    argument_names = \
        ['command_name']

    command_name: command_name_cls = command_name_cls
    """
    command_name argument of copy.
    """
