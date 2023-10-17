#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .command_name_1 import command_name as command_name_cls
from .tsv_file_name import tsv_file_name as tsv_file_name_cls
class export(Command):
    """
    Export execute-commands to a TSV file.
    
    Parameters
    ----------
        command_name : typing.List[str]
            'command_name' child.
        tsv_file_name : str
            'tsv_file_name' child.
    
    """

    fluent_name = "export"

    argument_names = \
        ['command_name', 'tsv_file_name']

    command_name: command_name_cls = command_name_cls
    """
    command_name argument of export.
    """
    tsv_file_name: tsv_file_name_cls = tsv_file_name_cls
    """
    tsv_file_name argument of export.
    """
