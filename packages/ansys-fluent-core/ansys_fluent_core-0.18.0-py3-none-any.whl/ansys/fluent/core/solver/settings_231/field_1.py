#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .width import width as width_cls
from .height import height as height_cls
class field(Command):
    """
    Set the field of view (width and height).
    
    Parameters
    ----------
        width : real
            'width' child.
        height : real
            'height' child.
    
    """

    fluent_name = "field"

    argument_names = \
        ['width', 'height']

    width: width_cls = width_cls
    """
    width argument of field.
    """
    height: height_cls = height_cls
    """
    height argument of field.
    """
