#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .type_1 import type as type_cls
from .two_dim_space import two_dim_space as two_dim_space_cls
from .velocity_formulation import velocity_formulation as velocity_formulation_cls
from .time import time as time_cls
class solver(Group):
    """
    'solver' child.
    """

    fluent_name = "solver"

    child_names = \
        ['type', 'two_dim_space', 'velocity_formulation', 'time']

    type: type_cls = type_cls
    """
    type child of solver.
    """
    two_dim_space: two_dim_space_cls = two_dim_space_cls
    """
    two_dim_space child of solver.
    """
    velocity_formulation: velocity_formulation_cls = velocity_formulation_cls
    """
    velocity_formulation child of solver.
    """
    time: time_cls = time_cls
    """
    time child of solver.
    """
