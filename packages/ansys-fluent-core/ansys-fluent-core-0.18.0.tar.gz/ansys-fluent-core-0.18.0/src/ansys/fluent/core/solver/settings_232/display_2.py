#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .object_name import object_name as object_name_cls
class display(Command):
    """
    Display graphics object.
    
    Parameters
    ----------
        object_name : str
            'object_name' child.
    
    """

    fluent_name = "display"

    argument_names = \
        ['object_name']

    object_name: object_name_cls = object_name_cls
    """
    object_name argument of display.
    """
