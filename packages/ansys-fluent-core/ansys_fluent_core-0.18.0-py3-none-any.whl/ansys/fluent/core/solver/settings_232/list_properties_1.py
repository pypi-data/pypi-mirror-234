#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .object_at import object_at as object_at_cls
class list_properties(Command):
    """
    'list_properties' command.
    
    Parameters
    ----------
        object_at : int
            'object_at' child.
    
    """

    fluent_name = "list-properties"

    argument_names = \
        ['object_at']

    object_at: object_at_cls = object_at_cls
    """
    object_at argument of list_properties.
    """
