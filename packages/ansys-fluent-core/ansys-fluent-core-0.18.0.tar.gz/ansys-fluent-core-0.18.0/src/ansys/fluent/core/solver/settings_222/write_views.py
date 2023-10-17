#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .file_name import file_name as file_name_cls
from .view_list import view_list as view_list_cls
class write_views(Command):
    """
    Write selected views to a view file.
    
    Parameters
    ----------
        file_name : str
            'file_name' child.
        view_list : typing.List[str]
            'view_list' child.
    
    """

    fluent_name = "write-views"

    argument_names = \
        ['file_name', 'view_list']

    file_name: file_name_cls = file_name_cls
    """
    file_name argument of write_views.
    """
    view_list: view_list_cls = view_list_cls
    """
    view_list argument of write_views.
    """
