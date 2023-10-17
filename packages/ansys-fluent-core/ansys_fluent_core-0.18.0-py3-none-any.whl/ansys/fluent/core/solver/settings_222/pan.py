#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .right import right as right_cls
from .up import up as up_cls
class pan(Command):
    """
    Adjust the camera position without modifying the position.
    
    Parameters
    ----------
        right : real
            'right' child.
        up : real
            'up' child.
    
    """

    fluent_name = "pan"

    argument_names = \
        ['right', 'up']

    right: right_cls = right_cls
    """
    right argument of pan.
    """
    up: up_cls = up_cls
    """
    up argument of pan.
    """
