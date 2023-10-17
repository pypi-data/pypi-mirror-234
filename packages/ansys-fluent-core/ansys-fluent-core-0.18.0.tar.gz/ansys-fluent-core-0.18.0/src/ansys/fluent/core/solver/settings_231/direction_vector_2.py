#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .x_component import x_component as x_component_cls
from .y_component import y_component as y_component_cls
from .z_component import z_component as z_component_cls
class direction_vector(Group):
    """
    'direction_vector' child.
    """

    fluent_name = "direction-vector"

    child_names = \
        ['x_component', 'y_component', 'z_component']

    x_component: x_component_cls = x_component_cls
    """
    x_component child of direction_vector.
    """
    y_component: y_component_cls = y_component_cls
    """
    y_component child of direction_vector.
    """
    z_component: z_component_cls = z_component_cls
    """
    z_component child of direction_vector.
    """
