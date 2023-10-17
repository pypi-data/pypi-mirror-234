#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .type_2 import type as type_cls
class projection(Command):
    """
    Set the camera projection.
    
    Parameters
    ----------
        type : str
            'type' child.
    
    """

    fluent_name = "projection"

    argument_names = \
        ['type']

    type: type_cls = type_cls
    """
    type argument of projection.
    """
