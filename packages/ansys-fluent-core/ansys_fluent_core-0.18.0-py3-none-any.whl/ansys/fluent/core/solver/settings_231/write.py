#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .file_type import file_type as file_type_cls
from .file_name_1 import file_name as file_name_cls
class write(Command):
    """
    'write' command.
    
    Parameters
    ----------
        file_type : str
            'file_type' child.
        file_name : str
            'file_name' child.
    
    """

    fluent_name = "write"

    argument_names = \
        ['file_type', 'file_name']

    file_type: file_type_cls = file_type_cls
    """
    file_type argument of write.
    """
    file_name: file_name_cls = file_name_cls
    """
    file_name argument of write.
    """
