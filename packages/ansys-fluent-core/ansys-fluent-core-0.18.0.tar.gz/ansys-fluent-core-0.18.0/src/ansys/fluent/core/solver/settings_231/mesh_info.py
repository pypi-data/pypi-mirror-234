#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .print_level import print_level as print_level_cls
class mesh_info(Command):
    """
    'mesh_info' command.
    
    Parameters
    ----------
        print_level : int
            Print zone information size.
    
    """

    fluent_name = "mesh-info"

    argument_names = \
        ['print_level']

    print_level: print_level_cls = print_level_cls
    """
    print_level argument of mesh_info.
    """
