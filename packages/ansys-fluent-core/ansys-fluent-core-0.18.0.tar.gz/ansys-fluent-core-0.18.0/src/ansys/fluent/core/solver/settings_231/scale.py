#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .x_scale import x_scale as x_scale_cls
from .y_scale import y_scale as y_scale_cls
from .z_scale import z_scale as z_scale_cls
class scale(Command):
    """
    'scale' command.
    
    Parameters
    ----------
        x_scale : real
            'x_scale' child.
        y_scale : real
            'y_scale' child.
        z_scale : real
            'z_scale' child.
    
    """

    fluent_name = "scale"

    argument_names = \
        ['x_scale', 'y_scale', 'z_scale']

    x_scale: x_scale_cls = x_scale_cls
    """
    x_scale argument of scale.
    """
    y_scale: y_scale_cls = y_scale_cls
    """
    y_scale argument of scale.
    """
    z_scale: z_scale_cls = z_scale_cls
    """
    z_scale argument of scale.
    """
