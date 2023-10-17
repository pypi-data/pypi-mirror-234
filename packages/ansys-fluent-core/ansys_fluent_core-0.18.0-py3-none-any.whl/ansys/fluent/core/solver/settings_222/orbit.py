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
class orbit(Command):
    """
    Adjust the camera position without modifying the target.
    
    Parameters
    ----------
        right : real
            'right' child.
        up : real
            'up' child.
    
    """

    fluent_name = "orbit"

    argument_names = \
        ['right', 'up']

    right: right_cls = right_cls
    """
    right argument of orbit.
    """
    up: up_cls = up_cls
    """
    up argument of orbit.
    """
