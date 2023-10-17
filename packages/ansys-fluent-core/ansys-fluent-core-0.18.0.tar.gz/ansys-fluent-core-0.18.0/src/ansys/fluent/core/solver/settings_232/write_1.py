#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .file_name_1 import file_name as file_name_cls
from .state_name_1 import state_name as state_name_cls
class write(Command):
    """
    Write display states to a file.
    
    Parameters
    ----------
        file_name : str
            'file_name' child.
        state_name : typing.List[str]
            'state_name' child.
    
    """

    fluent_name = "write"

    argument_names = \
        ['file_name', 'state_name']

    file_name: file_name_cls = file_name_cls
    """
    file_name argument of write.
    """
    state_name: state_name_cls = state_name_cls
    """
    state_name argument of write.
    """
