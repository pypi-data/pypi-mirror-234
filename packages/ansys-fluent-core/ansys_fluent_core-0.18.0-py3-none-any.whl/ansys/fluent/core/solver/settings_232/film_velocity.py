#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .list_properties_1 import list_properties as list_properties_cls
from .axis_direction_child import axis_direction_child

class film_velocity(ListObject[axis_direction_child]):
    """
    'film_velocity' child.
    """

    fluent_name = "film-velocity"

    command_names = \
        ['list_properties']

    list_properties: list_properties_cls = list_properties_cls
    """
    list_properties command of film_velocity.
    """
    child_object_type: axis_direction_child = axis_direction_child
    """
    child_object_type of film_velocity.
    """
