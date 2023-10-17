#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .name import name as name_cls
from .thread_name_list import thread_name_list as thread_name_list_cls
class mechanical_apdl(Command):
    """
    Write an Mechanical APDL file.
    
    Parameters
    ----------
        name : str
            'name' child.
        thread_name_list : typing.List[str]
            'thread_name_list' child.
    
    """

    fluent_name = "mechanical-apdl"

    argument_names = \
        ['name', 'thread_name_list']

    name: name_cls = name_cls
    """
    name argument of mechanical_apdl.
    """
    thread_name_list: thread_name_list_cls = thread_name_list_cls
    """
    thread_name_list argument of mechanical_apdl.
    """
