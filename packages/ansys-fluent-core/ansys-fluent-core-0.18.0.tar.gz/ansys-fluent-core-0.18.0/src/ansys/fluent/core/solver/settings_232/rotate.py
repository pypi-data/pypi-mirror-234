#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .angle import angle as angle_cls
from .origin import origin as origin_cls
from .axis_components import axis_components as axis_components_cls
class rotate(Command):
    """
    Rotate the mesh.
    
    Parameters
    ----------
        angle : real
            'angle' child.
        origin : typing.List[real]
            'origin' child.
        axis_components : typing.List[real]
            'axis_components' child.
    
    """

    fluent_name = "rotate"

    argument_names = \
        ['angle', 'origin', 'axis_components']

    angle: angle_cls = angle_cls
    """
    angle argument of rotate.
    """
    origin: origin_cls = origin_cls
    """
    origin argument of rotate.
    """
    axis_components: axis_components_cls = axis_components_cls
    """
    axis_components argument of rotate.
    """
