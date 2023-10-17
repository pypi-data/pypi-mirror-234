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
from .in_ import in_ as in__cls
class dolly(Command):
    """
    Adjust the camera position and target.
    
    Parameters
    ----------
        right : real
            'right' child.
        up : real
            'up' child.
        in_ : real
            'in' child.
    
    """

    fluent_name = "dolly"

    argument_names = \
        ['right', 'up', 'in_']

    right: right_cls = right_cls
    """
    right argument of dolly.
    """
    up: up_cls = up_cls
    """
    up argument of dolly.
    """
    in_: in__cls = in__cls
    """
    in_ argument of dolly.
    """
