#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .init_type import init_type as init_type_cls
class initialize(Command):
    """
    'initialize' command.
    
    Parameters
    ----------
        init_type : str
            'init_type' child.
    
    """

    fluent_name = "initialize"

    argument_names = \
        ['init_type']

    init_type: init_type_cls = init_type_cls
    """
    init_type argument of initialize.
    """
