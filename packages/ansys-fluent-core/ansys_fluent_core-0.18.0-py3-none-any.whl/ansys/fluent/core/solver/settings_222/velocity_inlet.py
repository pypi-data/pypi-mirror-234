#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .change_type import change_type as change_type_cls
from .velocity_inlet_child import velocity_inlet_child

class velocity_inlet(NamedObject[velocity_inlet_child], _CreatableNamedObjectMixin[velocity_inlet_child]):
    """
    'velocity_inlet' child.
    """

    fluent_name = "velocity-inlet"

    command_names = \
        ['change_type']

    change_type: change_type_cls = change_type_cls
    """
    change_type command of velocity_inlet.
    """
    child_object_type: velocity_inlet_child = velocity_inlet_child
    """
    child_object_type of velocity_inlet.
    """
